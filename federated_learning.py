"""
UVPFL Federated Learning Framework - Step 7

Implementation of Federated Learning for User Profile-Based Viewport Prediction
as described in the paper.

Key concepts from paper:
- FL is used to profile users separately based on head movement
- Data is stored on client side for training
- Each user can be trained separately and profiled independently
- FL enables privacy preservation in 360-degree video streaming

Paper quote: "We used FL for profiling users separately on the basis of 
their head movement in 360-degree videos."
"""

import os
import sys
import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import copy

# Import local modules
try:
    from model import UVPFLModel, create_resnet50_gru_model, EPOCHS, LEARNING_RATE, BATCH_SIZE
    from data_loader import UVPFLDataLoaderFast, SEQUENCE_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS
except ImportError:
    print("Warning: Could not import local modules. Some functionality may be limited.")


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class FederatedConfig:
    """Configuration for Federated Learning."""
    # Number of clients (users)
    num_clients: int = 50  # Paper uses 50 users
    
    # Number of federated rounds
    num_rounds: int = 10
    
    # Local epochs per round
    local_epochs: int = 5
    
    # Fraction of clients participating each round
    client_fraction: float = 0.2  # 20% of clients per round
    
    # Batch size for local training
    batch_size: int = 8
    
    # Learning rate
    learning_rate: float = 0.001
    
    # Model aggregation strategy
    aggregation_strategy: str = "fedavg"  # "fedavg" or "fedprox"
    
    # FedProx mu parameter (if using FedProx)
    fedprox_mu: float = 0.01
    
    # User profiling by video category
    profile_by_category: bool = True
    
    # Video categories from paper
    video_categories: List[str] = field(default_factory=lambda: [
        "NI_fast_paced",  # Natural-Image fast-paced
        "NI_slow_paced",  # Natural-Image slow-paced
        "CG_fast_paced"   # Computer-Generated fast-paced
    ])


# =============================================================================
# User Profile
# =============================================================================

@dataclass
class UserProfile:
    """
    User profile based on head movement behavior.
    
    Paper: "UVPFL profiles users based on their head movements for 
    different categories of videos."
    """
    user_id: str
    
    # Head movement statistics per video category
    head_movement_stats: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Average viewing patterns
    avg_yaw_velocity: float = 0.0
    avg_pitch_velocity: float = 0.0
    avg_roll_velocity: float = 0.0
    
    # Preferred viewport regions
    preferred_regions: Dict[str, float] = field(default_factory=dict)
    
    # Category preferences
    category_engagement: Dict[str, float] = field(default_factory=dict)
    
    # Model weights (local model)
    local_model_weights: Optional[List[np.ndarray]] = None
    
    # Training history
    training_history: List[Dict[str, float]] = field(default_factory=list)
    
    def update_from_orientation_data(self, orientation_data: np.ndarray, category: str):
        """
        Update profile from orientation data.
        
        Args:
            orientation_data: Array of [yaw, pitch, roll] values over time
            category: Video category
        """
        if len(orientation_data) < 2:
            return
        
        # Calculate velocities (rate of change)
        velocities = np.diff(orientation_data, axis=0)
        
        # Calculate statistics
        stats = {
            'mean_yaw_velocity': float(np.mean(np.abs(velocities[:, 0]))),
            'mean_pitch_velocity': float(np.mean(np.abs(velocities[:, 1]))),
            'mean_roll_velocity': float(np.mean(np.abs(velocities[:, 2]))),
            'std_yaw': float(np.std(orientation_data[:, 0])),
            'std_pitch': float(np.std(orientation_data[:, 1])),
            'std_roll': float(np.std(orientation_data[:, 2])),
            'max_yaw_velocity': float(np.max(np.abs(velocities[:, 0]))),
            'max_pitch_velocity': float(np.max(np.abs(velocities[:, 1]))),
        }
        
        self.head_movement_stats[category] = stats
        
        # Update overall averages
        all_stats = list(self.head_movement_stats.values())
        if all_stats:
            self.avg_yaw_velocity = np.mean([s['mean_yaw_velocity'] for s in all_stats])
            self.avg_pitch_velocity = np.mean([s['mean_pitch_velocity'] for s in all_stats])
            self.avg_roll_velocity = np.mean([s['mean_roll_velocity'] for s in all_stats])
    
    def similarity_to(self, other: 'UserProfile') -> float:
        """
        Calculate similarity to another user profile.
        
        Paper: "For high viewport prediction accuracy of a new user or a user 
        with no historical data, UVPFL bases its viewport prediction on the 
        viewport of similar users."
        
        Returns:
            Similarity score between 0 and 1
        """
        # Compare head movement statistics
        common_categories = set(self.head_movement_stats.keys()) & set(other.head_movement_stats.keys())
        
        if not common_categories:
            # Use overall averages if no common categories
            velocity_diff = np.sqrt(
                (self.avg_yaw_velocity - other.avg_yaw_velocity) ** 2 +
                (self.avg_pitch_velocity - other.avg_pitch_velocity) ** 2 +
                (self.avg_roll_velocity - other.avg_roll_velocity) ** 2
            )
            # Normalize to [0, 1] (assuming max velocity diff of 100)
            similarity = max(0, 1 - velocity_diff / 100)
        else:
            # Compare per-category statistics
            similarities = []
            for category in common_categories:
                my_stats = self.head_movement_stats[category]
                other_stats = other.head_movement_stats[category]
                
                # Euclidean distance in stat space
                diff = np.sqrt(
                    (my_stats['mean_yaw_velocity'] - other_stats['mean_yaw_velocity']) ** 2 +
                    (my_stats['mean_pitch_velocity'] - other_stats['mean_pitch_velocity']) ** 2 +
                    (my_stats['std_yaw'] - other_stats['std_yaw']) ** 2 +
                    (my_stats['std_pitch'] - other_stats['std_pitch']) ** 2
                )
                similarities.append(max(0, 1 - diff / 100))
            
            similarity = np.mean(similarities)
        
        return float(similarity)
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary for serialization."""
        return {
            'user_id': self.user_id,
            'head_movement_stats': self.head_movement_stats,
            'avg_yaw_velocity': self.avg_yaw_velocity,
            'avg_pitch_velocity': self.avg_pitch_velocity,
            'avg_roll_velocity': self.avg_roll_velocity,
            'preferred_regions': self.preferred_regions,
            'category_engagement': self.category_engagement,
            'training_history': self.training_history,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Create profile from dictionary."""
        profile = cls(user_id=data['user_id'])
        profile.head_movement_stats = data.get('head_movement_stats', {})
        profile.avg_yaw_velocity = data.get('avg_yaw_velocity', 0.0)
        profile.avg_pitch_velocity = data.get('avg_pitch_velocity', 0.0)
        profile.avg_roll_velocity = data.get('avg_roll_velocity', 0.0)
        profile.preferred_regions = data.get('preferred_regions', {})
        profile.category_engagement = data.get('category_engagement', {})
        profile.training_history = data.get('training_history', [])
        return profile


# =============================================================================
# Federated Client
# =============================================================================

class FederatedClient:
    """
    Represents a single client (user) in the federated learning system.
    
    Paper: "FL is a ML-based approach, where the data is stored on the 
    client side for training. The benefit of FL is that each user can be 
    trained separately and can be profiled independently."
    """
    
    def __init__(
        self,
        client_id: str,
        config: FederatedConfig,
        data_path: Optional[Path] = None
    ):
        """
        Initialize federated client.
        
        Args:
            client_id: Unique identifier for this client
            config: Federated learning configuration
            data_path: Path to client's local data
        """
        self.client_id = client_id
        self.config = config
        self.data_path = data_path
        
        # User profile
        self.profile = UserProfile(user_id=client_id)
        
        # Local model (initialized from global model)
        self.local_model: Optional[tf.keras.Model] = None
        
        # Local data (loaded on demand)
        self.local_data: Optional[Tuple[np.ndarray, np.ndarray]] = None
        
        # Training history
        self.history: List[Dict[str, float]] = []
    
    def load_local_data(self) -> bool:
        """
        Load client's local data.
        
        Returns:
            True if data loaded successfully
        """
        if self.data_path is None or not self.data_path.exists():
            return False
        
        try:
            # Load sequences and targets
            sequences_path = self.data_path / 'sequences.npy'
            targets_path = self.data_path / 'targets.npy'
            
            if sequences_path.exists() and targets_path.exists():
                X = np.load(sequences_path)
                y = np.load(targets_path)
                self.local_data = (X, y)
                return True
            
            # Alternative: load from individual sequence files
            sequence_files = sorted(self.data_path.glob('sequence_*.npy'))
            target_files = sorted(self.data_path.glob('target_*.npy'))
            
            if sequence_files and target_files:
                X = np.array([np.load(f) for f in sequence_files[:100]])  # Limit for memory
                y = np.array([np.load(f) for f in target_files[:100]])
                self.local_data = (X, y)
                return True
            
        except Exception as e:
            print(f"Client {self.client_id}: Error loading data - {e}")
        
        return False
    
    def set_model_weights(self, weights: List[np.ndarray]):
        """
        Set local model weights from global model.
        
        Args:
            weights: Model weights to set
        """
        if self.local_model is None:
            # Create local model
            self.local_model = create_resnet50_gru_model()
            self.local_model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
                loss='mse',
                metrics=['mae']
            )
        
        self.local_model.set_weights(weights)
    
    def get_model_weights(self) -> List[np.ndarray]:
        """Get local model weights."""
        if self.local_model is None:
            return []
        return self.local_model.get_weights()
    
    def train_local(
        self,
        global_weights: List[np.ndarray],
        epochs: Optional[int] = None
    ) -> Tuple[List[np.ndarray], int, Dict[str, float]]:
        """
        Train local model on client's data.
        
        Paper: "Our ML algorithm is performed separately on each client."
        
        Args:
            global_weights: Current global model weights
            epochs: Number of local epochs (default: config.local_epochs)
            
        Returns:
            Tuple of (updated weights, number of samples, training metrics)
        """
        epochs = epochs or self.config.local_epochs
        
        # Set weights from global model
        self.set_model_weights(global_weights)
        
        # Check if we have data
        if self.local_data is None:
            if not self.load_local_data():
                # Generate synthetic data for demonstration
                print(f"Client {self.client_id}: Using synthetic data")
                num_samples = 10
                X = np.random.rand(num_samples, SEQUENCE_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS).astype(np.float32)
                y = np.random.rand(num_samples, 3).astype(np.float32)  # [yaw, pitch, roll]
                self.local_data = (X, y)
        
        X, y = self.local_data
        num_samples = len(X)
        
        # Train locally
        history = self.local_model.fit(
            X, y,
            epochs=epochs,
            batch_size=self.config.batch_size,
            verbose=0,
            validation_split=0.1 if num_samples > 10 else 0.0
        )
        
        # Extract metrics
        metrics = {
            'loss': float(history.history['loss'][-1]),
            'mae': float(history.history.get('mae', [0])[-1]),
        }
        
        # Update profile training history
        self.profile.training_history.append({
            'round': len(self.history),
            'epochs': epochs,
            'samples': num_samples,
            **metrics
        })
        self.history.append(metrics)
        
        # Return updated weights
        return self.get_model_weights(), num_samples, metrics
    
    def update_profile_from_data(self, orientation_data: np.ndarray, category: str):
        """Update user profile from orientation data."""
        self.profile.update_from_orientation_data(orientation_data, category)


# =============================================================================
# Federated Server
# =============================================================================

class FederatedServer:
    """
    Federated Learning Server for coordinating training across clients.
    
    Implements FedAvg algorithm for model aggregation.
    """
    
    def __init__(self, config: FederatedConfig):
        """
        Initialize federated server.
        
        Args:
            config: Federated learning configuration
        """
        self.config = config
        
        # Global model
        self.global_model: Optional[tf.keras.Model] = None
        
        # Clients
        self.clients: Dict[str, FederatedClient] = {}
        
        # Training history
        self.round_history: List[Dict[str, Any]] = []
        
        # User profiles database
        self.user_profiles: Dict[str, UserProfile] = {}
    
    def initialize_global_model(self):
        """Initialize the global model."""
        print("Initializing global model...")
        self.global_model = create_resnet50_gru_model()
        self.global_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
            loss='mse',
            metrics=['mae']
        )
        print(f"Global model initialized with {self.global_model.count_params():,} parameters")
    
    def register_client(self, client: FederatedClient):
        """
        Register a client with the server.
        
        Args:
            client: Client to register
        """
        self.clients[client.client_id] = client
        self.user_profiles[client.client_id] = client.profile
    
    def create_clients_from_data(self, data_dir: Path) -> int:
        """
        Create clients from processed data directory.
        
        Args:
            data_dir: Directory containing user data
            
        Returns:
            Number of clients created
        """
        data_dir = Path(data_dir)
        
        # Look for user directories
        user_dirs = [d for d in data_dir.iterdir() if d.is_dir() and d.name.startswith('user_')]
        
        if not user_dirs:
            # Create synthetic clients
            print(f"No user directories found in {data_dir}. Creating {self.config.num_clients} synthetic clients.")
            for i in range(self.config.num_clients):
                client_id = f"user_{i:02d}"
                client = FederatedClient(client_id, self.config)
                self.register_client(client)
            return self.config.num_clients
        
        # Create clients from actual data
        for user_dir in user_dirs:
            client_id = user_dir.name
            client = FederatedClient(client_id, self.config, user_dir)
            self.register_client(client)
        
        print(f"Created {len(self.clients)} clients from data")
        return len(self.clients)
    
    def select_clients(self) -> List[FederatedClient]:
        """
        Select clients for current round.
        
        Returns:
            List of selected clients
        """
        num_clients = max(1, int(len(self.clients) * self.config.client_fraction))
        client_ids = list(self.clients.keys())
        selected_ids = np.random.choice(client_ids, size=num_clients, replace=False)
        return [self.clients[cid] for cid in selected_ids]
    
    def aggregate_weights(
        self,
        client_weights: List[Tuple[List[np.ndarray], int]]
    ) -> List[np.ndarray]:
        """
        Aggregate client weights using FedAvg.
        
        Paper: Uses Federated Learning for decentralized training.
        
        Args:
            client_weights: List of (weights, num_samples) tuples
            
        Returns:
            Aggregated weights
        """
        if not client_weights:
            return self.global_model.get_weights()
        
        # Calculate total samples
        total_samples = sum(n for _, n in client_weights)
        
        if total_samples == 0:
            return self.global_model.get_weights()
        
        # Weighted average of weights
        aggregated = []
        for layer_idx in range(len(client_weights[0][0])):
            layer_weights = []
            for weights, num_samples in client_weights:
                weight = num_samples / total_samples
                layer_weights.append(weights[layer_idx] * weight)
            aggregated.append(np.sum(layer_weights, axis=0))
        
        return aggregated
    
    def train_round(self, round_num: int) -> Dict[str, Any]:
        """
        Execute one round of federated training.
        
        Args:
            round_num: Current round number
            
        Returns:
            Round metrics
        """
        print(f"\n{'='*60}")
        print(f"Federated Round {round_num + 1}/{self.config.num_rounds}")
        print(f"{'='*60}")
        
        # Select clients
        selected_clients = self.select_clients()
        print(f"Selected {len(selected_clients)} clients for this round")
        
        # Get current global weights
        global_weights = self.global_model.get_weights()
        
        # Train each client
        client_results = []
        for client in selected_clients:
            print(f"  Training client {client.client_id}...", end=" ")
            try:
                weights, num_samples, metrics = client.train_local(global_weights)
                client_results.append((weights, num_samples))
                print(f"loss: {metrics['loss']:.4f}, samples: {num_samples}")
            except Exception as e:
                print(f"failed: {e}")
        
        # Aggregate weights
        if client_results:
            aggregated_weights = self.aggregate_weights(client_results)
            self.global_model.set_weights(aggregated_weights)
        
        # Calculate round metrics
        avg_loss = np.mean([c.history[-1]['loss'] for c in selected_clients if c.history])
        total_samples = sum(n for _, n in client_results)
        
        round_metrics = {
            'round': round_num + 1,
            'num_clients': len(selected_clients),
            'total_samples': total_samples,
            'avg_loss': float(avg_loss) if not np.isnan(avg_loss) else 0.0,
        }
        
        self.round_history.append(round_metrics)
        print(f"Round {round_num + 1} complete. Avg loss: {round_metrics['avg_loss']:.4f}")
        
        return round_metrics
    
    def train(self, num_rounds: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Run full federated training.
        
        Args:
            num_rounds: Number of rounds (default: config.num_rounds)
            
        Returns:
            Training history
        """
        num_rounds = num_rounds or self.config.num_rounds
        
        # Initialize global model if needed
        if self.global_model is None:
            self.initialize_global_model()
        
        # Create clients if needed
        if not self.clients:
            self.create_clients_from_data(Path('processed_data'))
        
        print(f"\nStarting Federated Training")
        print(f"Clients: {len(self.clients)}")
        print(f"Rounds: {num_rounds}")
        print(f"Local epochs: {self.config.local_epochs}")
        print(f"Client fraction: {self.config.client_fraction}")
        
        # Training loop
        for round_num in range(num_rounds):
            self.train_round(round_num)
        
        print(f"\n{'='*60}")
        print("Federated Training Complete!")
        print(f"{'='*60}")
        
        return self.round_history
    
    def find_similar_users(self, user_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find similar users for viewport prediction.
        
        Paper: "For high viewport prediction accuracy of a new user or a user 
        with no historical data, UVPFL bases its viewport prediction on the 
        viewport of similar users."
        
        Args:
            user_id: ID of user to find similar users for
            top_k: Number of similar users to return
            
        Returns:
            List of (user_id, similarity_score) tuples
        """
        if user_id not in self.user_profiles:
            return []
        
        target_profile = self.user_profiles[user_id]
        similarities = []
        
        for other_id, other_profile in self.user_profiles.items():
            if other_id != user_id:
                sim = target_profile.similarity_to(other_profile)
                similarities.append((other_id, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def save_model(self, path: str = 'checkpoints/federated_global_model.keras'):
        """Save the global model."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.global_model.save(path)
        print(f"Global model saved to {path}")
    
    def save_profiles(self, path: str = 'checkpoints/user_profiles.json'):
        """Save all user profiles."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        profiles_dict = {uid: p.to_dict() for uid, p in self.user_profiles.items()}
        with open(path, 'w') as f:
            json.dump(profiles_dict, f, indent=2)
        print(f"User profiles saved to {path}")
    
    def load_profiles(self, path: str = 'checkpoints/user_profiles.json'):
        """Load user profiles from file."""
        with open(path, 'r') as f:
            profiles_dict = json.load(f)
        self.user_profiles = {uid: UserProfile.from_dict(p) for uid, p in profiles_dict.items()}
        print(f"Loaded {len(self.user_profiles)} user profiles")


# =============================================================================
# Main Execution
# =============================================================================

def run_federated_learning(
    data_dir: str = 'processed_data',
    num_rounds: int = 10,
    local_epochs: int = 5,
    client_fraction: float = 0.2,
    save_model: bool = True
) -> FederatedServer:
    """
    Run complete federated learning pipeline.
    
    Args:
        data_dir: Directory containing processed data
        num_rounds: Number of federated rounds
        local_epochs: Local epochs per round
        client_fraction: Fraction of clients per round
        save_model: Whether to save the model
        
    Returns:
        Trained FederatedServer instance
    """
    # Configuration
    config = FederatedConfig(
        num_rounds=num_rounds,
        local_epochs=local_epochs,
        client_fraction=client_fraction,
    )
    
    # Create server
    server = FederatedServer(config)
    
    # Initialize model
    server.initialize_global_model()
    
    # Create clients
    server.create_clients_from_data(Path(data_dir))
    
    # Train
    history = server.train()
    
    # Save
    if save_model:
        server.save_model()
        server.save_profiles()
    
    return server


def test_federated_learning():
    """Quick test of federated learning components."""
    print("=" * 60)
    print("Testing UVPFL Federated Learning (Step 7)")
    print("=" * 60)
    
    # Create configuration
    config = FederatedConfig(
        num_clients=5,
        num_rounds=2,
        local_epochs=1,
        client_fraction=0.4,
    )
    
    # Create server
    server = FederatedServer(config)
    
    # Initialize model
    server.initialize_global_model()
    
    # Create synthetic clients
    for i in range(config.num_clients):
        client = FederatedClient(f"user_{i:02d}", config)
        server.register_client(client)
    
    print(f"\n✅ Created {len(server.clients)} clients")
    
    # Run one round
    print("\n📊 Running one federated round...")
    metrics = server.train_round(0)
    print(f"✅ Round complete: {metrics}")
    
    # Test similar user finding
    print("\n🔍 Testing similar user finding...")
    # Add some fake profile data
    for uid, profile in server.user_profiles.items():
        profile.avg_yaw_velocity = np.random.rand() * 10
        profile.avg_pitch_velocity = np.random.rand() * 10
    
    similar = server.find_similar_users("user_00", top_k=3)
    print(f"✅ Similar users to user_00: {similar}")
    
    print("\n" + "=" * 60)
    print("✅ Federated Learning Test Complete!")
    print("=" * 60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='UVPFL Federated Learning')
    parser.add_argument('--test', action='store_true', help='Run quick test')
    parser.add_argument('--rounds', type=int, default=10, help='Number of rounds')
    parser.add_argument('--local_epochs', type=int, default=5, help='Local epochs')
    parser.add_argument('--data_dir', type=str, default='processed_data', help='Data directory')
    
    args = parser.parse_args()
    
    if args.test:
        test_federated_learning()
    else:
        run_federated_learning(
            data_dir=args.data_dir,
            num_rounds=args.rounds,
            local_epochs=args.local_epochs,
        )

