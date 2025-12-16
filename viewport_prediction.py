"""
UVPFL Viewport Prediction & Similar User Matching

Implementation of the core UVPFL algorithm as described in the paper:
1. Similar user matching based on head movement profiles
2. Viewport prediction using pre-trained model
3. Viewport comparison and merging (γ = 80% overlap threshold)
4. Tile probability calculation using Equation (1)

Paper Algorithm 1 - Phase 2: Viewport Prediction
- Calculate Y, PI, R for User
- Calculate head movement speed
- Predict viewport Vp using pre-trained ML model
- If Vp ∩ Vs ≥ γ % then merge Vp and Vs
- Calculate tile visibility probability
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from scipy.spatial.distance import cosine, euclidean
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass
import math


# ============================================================================
# CONFIGURATION (from paper)
# ============================================================================
GAMMA = 0.80  # Overlap threshold (80% as per paper)
TILE_SIZE = 192  # Tile size in pixels (from dataset readme)

# Viewport parameters (typical VR headset FoV)
VIEWPORT_H_FOV = 110  # Horizontal Field of View in degrees (90-120 typical)
VIEWPORT_V_FOV = 90   # Vertical Field of View in degrees

# Video dimensions (equirectangular projection)
VIDEO_WIDTH = 3840    # 4K width
VIDEO_HEIGHT = 1920   # 4K height (2:1 aspect ratio for 360°)

# Tile grid (calculated from tile size)
NUM_TILES_H = VIDEO_WIDTH // TILE_SIZE   # 20 tiles horizontally
NUM_TILES_V = VIDEO_HEIGHT // TILE_SIZE  # 10 tiles vertically


@dataclass
class UserProfile:
    """User profile for similarity matching."""
    user_id: int
    video_name: str
    category: str
    mean_yaw: float
    std_yaw: float
    mean_pitch: float
    std_pitch: float
    mean_roll: float
    std_roll: float
    mean_speed: float
    std_speed: float
    num_frames: int = 0
    
    def to_feature_vector(self) -> np.ndarray:
        """Convert profile to feature vector for similarity calculation."""
        return np.array([
            self.mean_yaw, self.std_yaw,
            self.mean_pitch, self.std_pitch,
            self.mean_roll, self.std_roll,
            self.mean_speed, self.std_speed
        ])


@dataclass
class Viewport:
    """Viewport representation."""
    yaw: float      # Yaw angle (horizontal rotation) in degrees
    pitch: float    # Pitch angle (vertical rotation) in degrees
    roll: float     # Roll angle (tilt) in degrees
    h_fov: float = VIEWPORT_H_FOV  # Horizontal FoV
    v_fov: float = VIEWPORT_V_FOV  # Vertical FoV
    
    def get_center(self) -> Tuple[float, float]:
        """Get viewport center in (yaw, pitch) coordinates."""
        return (self.yaw, self.pitch)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get viewport bounds as (left, right, top, bottom) in degrees.
        Yaw: -180 to 180 (horizontal)
        Pitch: -90 to 90 (vertical)
        """
        left = self.yaw - self.h_fov / 2
        right = self.yaw + self.h_fov / 2
        top = min(90, self.pitch + self.v_fov / 2)
        bottom = max(-90, self.pitch - self.v_fov / 2)
        
        return (left, right, top, bottom)
    
    def to_pixel_coords(self, video_width: int = VIDEO_WIDTH, 
                        video_height: int = VIDEO_HEIGHT) -> Tuple[int, int, int, int]:
        """
        Convert viewport bounds to pixel coordinates.
        
        Returns:
            (x_min, x_max, y_min, y_max) in pixels
        """
        left, right, top, bottom = self.get_bounds()
        
        # Convert yaw (-180 to 180) to x (0 to width)
        x_min = int((left + 180) / 360 * video_width) % video_width
        x_max = int((right + 180) / 360 * video_width) % video_width
        
        # Convert pitch (-90 to 90) to y (0 to height)
        # Note: pitch increases upward, but y increases downward
        y_min = int((90 - top) / 180 * video_height)
        y_max = int((90 - bottom) / 180 * video_height)
        
        return (x_min, x_max, y_min, y_max)


class SimilarUserMatcher:
    """
    Matches users based on head movement profiles.
    
    Paper: "UVPFL profiles users based on their head movements for different 
    categories of videos. For high viewport prediction accuracy of a new user 
    or a user with no historical data, UVPFL bases its viewport prediction on 
    the viewport of similar users."
    """
    
    def __init__(self, processed_path: str = 'processed_data'):
        """
        Initialize the similar user matcher.
        
        Args:
            processed_path: Path to processed data with user profiles
        """
        self.processed_path = Path(processed_path)
        self.profiles = {}  # category -> list of UserProfile
        self._load_profiles()
    
    def _load_profiles(self):
        """Load user profiles from processed data."""
        profiles_path = self.processed_path / 'user_profiles'
        
        for profile_file in profiles_path.glob('*.json'):
            category = profile_file.stem  # e.g., 'cg_fast_paced'
            
            with open(profile_file, 'r') as f:
                profiles_data = json.load(f)
            
            self.profiles[category] = []
            for p in profiles_data:
                profile = UserProfile(
                    user_id=p['user_id'],
                    video_name=p['video_name'],
                    category=p['category'],
                    mean_yaw=p['mean_yaw'],
                    std_yaw=p['std_yaw'],
                    mean_pitch=p['mean_pitch'],
                    std_pitch=p['std_pitch'],
                    mean_roll=p['mean_roll'],
                    std_roll=p['std_roll'],
                    mean_speed=p['mean_speed'],
                    std_speed=p['std_speed'],
                    num_frames=p.get('num_frames', 0)
                )
                self.profiles[category].append(profile)
        
        print(f"Loaded profiles for {len(self.profiles)} categories")
        for cat, profiles in self.profiles.items():
            print(f"  - {cat}: {len(profiles)} profiles")
    
    def find_similar_users(self, 
                           current_profile: UserProfile,
                           category: str,
                           exclude_user: int = None,
                           top_k: int = 5) -> List[Tuple[UserProfile, float]]:
        """
        Find similar users based on head movement profiles.
        
        Paper: "similar users tend to have similar viewing behaviour while 
        watching 360-degree videos"
        
        Args:
            current_profile: Profile of the current user
            category: Video category to search within
            exclude_user: User ID to exclude (usually the current user)
            top_k: Number of similar users to return
            
        Returns:
            List of (profile, similarity_score) tuples, sorted by similarity
        """
        if category not in self.profiles:
            return []
        
        current_features = current_profile.to_feature_vector()
        
        similarities = []
        for profile in self.profiles[category]:
            # Skip the current user
            if exclude_user and profile.user_id == exclude_user:
                continue
            
            # Calculate similarity using cosine similarity
            profile_features = profile.to_feature_vector()
            
            # Normalize features
            current_norm = current_features / (np.linalg.norm(current_features) + 1e-8)
            profile_norm = profile_features / (np.linalg.norm(profile_features) + 1e-8)
            
            # Cosine similarity
            similarity = np.dot(current_norm, profile_norm)
            
            similarities.append((profile, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_similar_user_viewports(self,
                                   similar_users: List[Tuple[UserProfile, float]],
                                   frame_idx: int) -> List[Tuple[Viewport, float]]:
        """
        Get viewports of similar users at a specific frame.
        
        Args:
            similar_users: List of (profile, similarity) tuples
            frame_idx: Frame index to get viewport for
            
        Returns:
            List of (viewport, weight) tuples
        """
        viewports = []
        
        for profile, similarity in similar_users:
            # Load orientation data for this user-video pair
            user_dir = (self.processed_path / profile.category / 
                       profile.video_name / f'user{profile.user_id:02d}')
            orientation_path = user_dir / 'orientation.npy'
            
            if not orientation_path.exists():
                continue
            
            orientation = np.load(orientation_path)
            
            if frame_idx >= len(orientation):
                continue
            
            yaw, pitch, roll = orientation[frame_idx]
            viewport = Viewport(yaw=yaw, pitch=pitch, roll=roll)
            
            viewports.append((viewport, similarity))
        
        return viewports


class ViewportPredictor:
    """
    Main viewport prediction class implementing the UVPFL algorithm.
    
    Algorithm 1 - Phase 2: Viewport Prediction
    """
    
    def __init__(self, 
                 model=None,
                 processed_path: str = 'processed_data',
                 gamma: float = GAMMA):
        """
        Initialize the viewport predictor.
        
        Args:
            model: Trained UVPFL model (or None for testing)
            processed_path: Path to processed data
            gamma: Overlap threshold (default: 0.80 = 80%)
        """
        self.model = model
        self.gamma = gamma
        self.similar_user_matcher = SimilarUserMatcher(processed_path)
    
    def predict_viewport(self, 
                         frames: np.ndarray,
                         current_orientation: np.ndarray) -> Viewport:
        """
        Predict viewport using the trained model.
        
        Args:
            frames: Input frame sequence (sequence_length, height, width, channels)
            current_orientation: Current (yaw, pitch, roll)
            
        Returns:
            Predicted Viewport
        """
        if self.model is None:
            # Fallback: use current orientation as prediction
            return Viewport(
                yaw=current_orientation[0],
                pitch=current_orientation[1],
                roll=current_orientation[2]
            )
        
        # Add batch dimension if needed
        if frames.ndim == 4:
            frames = np.expand_dims(frames, axis=0)
        
        # Predict
        prediction = self.model.predict(frames, verbose=0)
        
        # Get predicted orientation change (delta)
        delta_yaw, delta_pitch, delta_roll = prediction[0]
        
        # Apply delta to current orientation
        predicted_yaw = current_orientation[0] + delta_yaw
        predicted_pitch = current_orientation[1] + delta_pitch
        predicted_roll = current_orientation[2] + delta_roll
        
        return Viewport(
            yaw=predicted_yaw,
            pitch=predicted_pitch,
            roll=predicted_roll
        )
    
    def calculate_viewport_overlap(self, vp1: Viewport, vp2: Viewport) -> float:
        """
        Calculate overlap between two viewports.
        
        Paper: "If the overlapping area of VP and VS is greater than γ, 
        then UVPFL merges VP and VS"
        
        Args:
            vp1: First viewport
            vp2: Second viewport
            
        Returns:
            Overlap ratio (0 to 1)
        """
        # Get bounds
        left1, right1, top1, bottom1 = vp1.get_bounds()
        left2, right2, top2, bottom2 = vp2.get_bounds()
        
        # Handle wrap-around for yaw (horizontal)
        # Normalize to 0-360 range for easier calculation
        def normalize_yaw(y):
            return (y + 180) % 360
        
        left1_n, right1_n = normalize_yaw(left1), normalize_yaw(right1)
        left2_n, right2_n = normalize_yaw(left2), normalize_yaw(right2)
        
        # Calculate horizontal overlap
        if right1_n < left1_n:  # Wrap around
            h_overlap = max(0, min(right1_n, right2_n) - max(0, left2_n)) + \
                       max(0, min(360, right2_n) - max(left1_n, left2_n))
        elif right2_n < left2_n:  # Wrap around
            h_overlap = max(0, min(right1_n, 360) - max(left1_n, left2_n)) + \
                       max(0, min(right1_n, right2_n) - max(0, left1_n))
        else:
            h_overlap = max(0, min(right1_n, right2_n) - max(left1_n, left2_n))
        
        # Calculate vertical overlap
        v_overlap = max(0, min(top1, top2) - max(bottom1, bottom2))
        
        # Calculate areas
        area1 = vp1.h_fov * vp1.v_fov
        area2 = vp2.h_fov * vp2.v_fov
        overlap_area = h_overlap * v_overlap
        
        # Overlap ratio (intersection over union or intersection over min area)
        overlap_ratio = overlap_area / min(area1, area2) if min(area1, area2) > 0 else 0
        
        return min(1.0, overlap_ratio)
    
    def merge_viewports(self, vp: Viewport, vs: Viewport, 
                        weight_vp: float = 0.6, weight_vs: float = 0.4) -> Viewport:
        """
        Merge predicted viewport (Vp) with similar user viewport (Vs).
        
        Paper: "If Vp ∩ Vs ≥ γ % then Merge Vp and Vs"
        
        Args:
            vp: Predicted viewport
            vs: Similar user viewport
            weight_vp: Weight for predicted viewport
            weight_vs: Weight for similar user viewport
            
        Returns:
            Merged viewport
        """
        # Weighted average of orientations
        merged_yaw = weight_vp * vp.yaw + weight_vs * vs.yaw
        merged_pitch = weight_vp * vp.pitch + weight_vs * vs.pitch
        merged_roll = weight_vp * vp.roll + weight_vs * vs.roll
        
        return Viewport(
            yaw=merged_yaw,
            pitch=merged_pitch,
            roll=merged_roll
        )
    
    def predict_with_similar_users(self,
                                   frames: np.ndarray,
                                   current_orientation: np.ndarray,
                                   current_profile: UserProfile,
                                   frame_idx: int,
                                   top_k_users: int = 3) -> Tuple[Viewport, bool]:
        """
        Predict viewport using model and similar users.
        
        This implements the core UVPFL algorithm from the paper.
        
        Args:
            frames: Input frame sequence
            current_orientation: Current (yaw, pitch, roll)
            current_profile: Current user's profile
            frame_idx: Current frame index
            top_k_users: Number of similar users to consider
            
        Returns:
            Tuple of (final_viewport, was_merged)
        """
        # Step 1: Predict viewport using ML model
        vp = self.predict_viewport(frames, current_orientation)
        
        # Step 2: Find similar users
        similar_users = self.similar_user_matcher.find_similar_users(
            current_profile,
            current_profile.category,
            exclude_user=current_profile.user_id,
            top_k=top_k_users
        )
        
        if not similar_users:
            return vp, False
        
        # Step 3: Get viewports of similar users
        similar_viewports = self.similar_user_matcher.get_similar_user_viewports(
            similar_users, frame_idx
        )
        
        if not similar_viewports:
            return vp, False
        
        # Step 4: Check overlap with each similar user viewport
        was_merged = False
        for vs, weight in similar_viewports:
            overlap = self.calculate_viewport_overlap(vp, vs)
            
            # If overlap >= gamma, merge viewports
            if overlap >= self.gamma:
                vp = self.merge_viewports(vp, vs, weight_vp=0.6, weight_vs=0.4 * weight)
                was_merged = True
                break  # Merge with the most similar user only
        
        return vp, was_merged


class TileProbabilityCalculator:
    """
    Calculate tile visibility probabilities.
    
    Paper Equation (1): Plk = P_θlk · P_φlk
    
    Groups tiles by probability:
    - Group 1: Viewport tiles (VP)
    - Group 2: Probability > 98%
    - Group 3: Probability 95-98%
    - Group 4: Probability 90-95%
    """
    
    def __init__(self,
                 video_width: int = VIDEO_WIDTH,
                 video_height: int = VIDEO_HEIGHT,
                 tile_size: int = TILE_SIZE):
        """
        Initialize the tile probability calculator.
        
        Args:
            video_width: Video width in pixels
            video_height: Video height in pixels
            tile_size: Tile size in pixels
        """
        self.video_width = video_width
        self.video_height = video_height
        self.tile_size = tile_size
        self.num_tiles_h = video_width // tile_size
        self.num_tiles_v = video_height // tile_size
    
    def get_tile_center(self, tile_l: int, tile_k: int) -> Tuple[float, float]:
        """
        Get the center of a tile in (yaw, pitch) coordinates.
        
        Args:
            tile_l: Tile row index (0 to num_tiles_v - 1)
            tile_k: Tile column index (0 to num_tiles_h - 1)
            
        Returns:
            (yaw, pitch) in degrees
        """
        # Calculate pixel center
        center_x = (tile_k + 0.5) * self.tile_size
        center_y = (tile_l + 0.5) * self.tile_size
        
        # Convert to spherical coordinates
        yaw = (center_x / self.video_width) * 360 - 180
        pitch = 90 - (center_y / self.video_height) * 180
        
        return (yaw, pitch)
    
    def calculate_tile_probability(self,
                                   viewport: Viewport,
                                   tile_l: int,
                                   tile_k: int,
                                   sigma_theta: float = 15.0,
                                   sigma_phi: float = 10.0) -> float:
        """
        Calculate visibility probability for a tile.
        
        Based on Paper Equation (1) with Gaussian distribution assumption.
        
        Args:
            viewport: Current viewport
            tile_l: Tile row index
            tile_k: Tile column index
            sigma_theta: Standard deviation for yaw (degrees)
            sigma_phi: Standard deviation for pitch (degrees)
            
        Returns:
            Probability (0 to 1)
        """
        tile_yaw, tile_pitch = self.get_tile_center(tile_l, tile_k)
        
        # Angular distance from viewport center
        delta_theta = abs(tile_yaw - viewport.yaw)
        delta_phi = abs(tile_pitch - viewport.pitch)
        
        # Handle wrap-around for yaw
        if delta_theta > 180:
            delta_theta = 360 - delta_theta
        
        # Gaussian probability
        p_theta = np.exp(-(delta_theta ** 2) / (2 * sigma_theta ** 2))
        p_phi = np.exp(-(delta_phi ** 2) / (2 * sigma_phi ** 2))
        
        return p_theta * p_phi
    
    def get_viewport_tiles(self, viewport: Viewport) -> List[Tuple[int, int]]:
        """
        Get tiles that fall within the viewport.
        
        Args:
            viewport: Current viewport
            
        Returns:
            List of (tile_l, tile_k) tuples
        """
        viewport_tiles = []
        
        for l in range(self.num_tiles_v):
            for k in range(self.num_tiles_h):
                tile_yaw, tile_pitch = self.get_tile_center(l, k)
                
                # Check if tile center is within viewport
                delta_yaw = abs(tile_yaw - viewport.yaw)
                if delta_yaw > 180:
                    delta_yaw = 360 - delta_yaw
                
                delta_pitch = abs(tile_pitch - viewport.pitch)
                
                if delta_yaw <= viewport.h_fov / 2 and delta_pitch <= viewport.v_fov / 2:
                    viewport_tiles.append((l, k))
        
        return viewport_tiles
    
    def get_tile_groups(self, viewport: Viewport) -> Dict[str, List[Tuple[int, int, float]]]:
        """
        Group tiles by visibility probability.
        
        Paper: "Group one tiles represent VP; Group two tiles have probability 
        higher than 98%; Group three tiles have probability between 95% and 98%; 
        Group four tiles have probability between 90% and 95%"
        
        Args:
            viewport: Current viewport
            
        Returns:
            Dictionary with groups: 'viewport', 'high' (>98%), 'medium' (95-98%), 
            'low' (90-95%), containing (tile_l, tile_k, probability) tuples
        """
        groups = {
            'viewport': [],     # Group 1: VP tiles
            'high': [],         # Group 2: > 98%
            'medium': [],       # Group 3: 95-98%
            'low': [],          # Group 4: 90-95%
            'neighboring': []   # Additional neighboring tiles
        }
        
        # Get viewport tiles
        viewport_tiles = set(self.get_viewport_tiles(viewport))
        
        for l in range(self.num_tiles_v):
            for k in range(self.num_tiles_h):
                prob = self.calculate_tile_probability(viewport, l, k)
                
                if (l, k) in viewport_tiles:
                    groups['viewport'].append((l, k, prob))
                elif prob > 0.98:
                    groups['high'].append((l, k, prob))
                elif prob > 0.95:
                    groups['medium'].append((l, k, prob))
                elif prob > 0.90:
                    groups['low'].append((l, k, prob))
                elif prob > 0.80:
                    groups['neighboring'].append((l, k, prob))
        
        return groups


def calculate_prediction_accuracy(predicted: Viewport, 
                                  actual: Viewport,
                                  tile_calculator: TileProbabilityCalculator = None) -> Dict:
    """
    Calculate prediction accuracy metrics.
    
    Paper metrics:
    - Accuracy: overlap of predicted and actual viewport
    - Precision: correctly predicted tiles / total predicted tiles
    - Recall: correctly predicted tiles / actual viewed tiles
    
    Args:
        predicted: Predicted viewport
        actual: Actual viewport
        tile_calculator: TileProbabilityCalculator instance
        
    Returns:
        Dictionary with accuracy metrics
    """
    if tile_calculator is None:
        tile_calculator = TileProbabilityCalculator()
    
    # Get tiles for each viewport
    predicted_tiles = set(tile_calculator.get_viewport_tiles(predicted))
    actual_tiles = set(tile_calculator.get_viewport_tiles(actual))
    
    # Calculate metrics
    intersection = predicted_tiles & actual_tiles
    union = predicted_tiles | actual_tiles
    
    # Tile-based accuracy (IoU)
    accuracy = len(intersection) / len(union) if len(union) > 0 else 0
    
    # Precision: correctly predicted / total predicted
    precision = len(intersection) / len(predicted_tiles) if len(predicted_tiles) > 0 else 0
    
    # Recall: correctly predicted / actual
    recall = len(intersection) / len(actual_tiles) if len(actual_tiles) > 0 else 0
    
    # Angular error
    angular_error = np.sqrt(
        (predicted.yaw - actual.yaw) ** 2 + 
        (predicted.pitch - actual.pitch) ** 2
    )
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'angular_error': angular_error,
        'predicted_tiles': len(predicted_tiles),
        'actual_tiles': len(actual_tiles),
        'intersection_tiles': len(intersection)
    }


def test_viewport_prediction():
    """Test the viewport prediction system."""
    print("=" * 60)
    print("Testing UVPFL Viewport Prediction System")
    print("=" * 60)
    
    # Test Similar User Matcher
    print("\n1. Testing Similar User Matcher...")
    matcher = SimilarUserMatcher('processed_data')
    
    # Create a test profile
    test_profile = UserProfile(
        user_id=1,
        video_name='pacman',
        category='cg_fast_paced',
        mean_yaw=0.5,
        std_yaw=10.0,
        mean_pitch=2.0,
        std_pitch=5.0,
        mean_roll=0.0,
        std_roll=2.0,
        mean_speed=1.5,
        std_speed=0.8
    )
    
    similar_users = matcher.find_similar_users(test_profile, 'cg_fast_paced', top_k=3)
    print(f"   Found {len(similar_users)} similar users")
    for profile, similarity in similar_users[:3]:
        print(f"   - User {profile.user_id} ({profile.video_name}): similarity={similarity:.3f}")
    
    # Test Viewport operations
    print("\n2. Testing Viewport Operations...")
    vp1 = Viewport(yaw=10.0, pitch=5.0, roll=0.0)
    vp2 = Viewport(yaw=15.0, pitch=8.0, roll=0.0)
    
    predictor = ViewportPredictor(model=None, processed_path='processed_data')
    overlap = predictor.calculate_viewport_overlap(vp1, vp2)
    print(f"   Viewport 1: yaw={vp1.yaw}, pitch={vp1.pitch}")
    print(f"   Viewport 2: yaw={vp2.yaw}, pitch={vp2.pitch}")
    print(f"   Overlap: {overlap:.2%}")
    
    # Test merge
    merged = predictor.merge_viewports(vp1, vp2)
    print(f"   Merged: yaw={merged.yaw:.1f}, pitch={merged.pitch:.1f}")
    
    # Test Tile Probability Calculator
    print("\n3. Testing Tile Probability Calculator...")
    tile_calc = TileProbabilityCalculator()
    
    viewport = Viewport(yaw=0.0, pitch=0.0, roll=0.0)
    groups = tile_calc.get_tile_groups(viewport)
    
    print(f"   Viewport tiles: {len(groups['viewport'])}")
    print(f"   High prob (>98%): {len(groups['high'])}")
    print(f"   Medium prob (95-98%): {len(groups['medium'])}")
    print(f"   Low prob (90-95%): {len(groups['low'])}")
    
    # Test accuracy calculation
    print("\n4. Testing Accuracy Calculation...")
    predicted = Viewport(yaw=10.0, pitch=5.0, roll=0.0)
    actual = Viewport(yaw=12.0, pitch=6.0, roll=0.0)
    
    metrics = calculate_prediction_accuracy(predicted, actual, tile_calc)
    print(f"   Accuracy: {metrics['accuracy']:.2%}")
    print(f"   Precision: {metrics['precision']:.2%}")
    print(f"   Recall: {metrics['recall']:.2%}")
    print(f"   Angular error: {metrics['angular_error']:.2f}°")
    
    print("\n" + "=" * 60)
    print("✅ Viewport prediction system test passed!")
    print("=" * 60)


if __name__ == '__main__':
    test_viewport_prediction()

