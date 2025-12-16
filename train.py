"""
UVPFL Training Pipeline

Complete training script for the UVPFL model as described in the paper:
- Model: ResNet50 + GRU
- Optimizer: Adam
- Loss: Mean Squared Error (MSE)
- Epochs: 50 (paper: "After 50 epochs, there is much less change in accuracy")
- Best results: 96% accuracy with ResNet50

Paper training setup:
- Input shape: (30, 120, 240, 3)
- Adam optimizer, MSE loss
- 50 epochs
- Tested: AlexNet (73%), MobileNet (56%), ResNet50 (96%)
"""

import os
import sys
import json
import argparse
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional

# Enable GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

from data_loader import UVPFLDataLoaderFast, SEQUENCE_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS
from model import UVPFLModel, get_callbacks, EPOCHS, LEARNING_RATE, BATCH_SIZE


def print_gpu_info():
    """Print GPU information."""
    print("=" * 60)
    print("GPU Information")
    print("=" * 60)
    
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"Number of GPUs: {len(gpus)}")
        for gpu in gpus:
            print(f"  - {gpu.name}")
        
        # Get memory info
        import subprocess
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader'],
            capture_output=True, text=True
        )
        print(f"GPU Details: {result.stdout.strip()}")
    else:
        print("No GPU available, using CPU")
    
    print("=" * 60)


def create_training_config(args) -> Dict:
    """Create training configuration."""
    config = {
        'model_type': args.model_type,
        'batch_size': args.batch_size,
        'epochs': args.epochs,
        'learning_rate': args.learning_rate,
        'sequence_length': SEQUENCE_LENGTH,
        'frame_height': FRAME_HEIGHT,
        'frame_width': FRAME_WIDTH,
        'channels': CHANNELS,
        'freeze_backbone': not args.unfreeze_backbone,
        'gru_units': args.gru_units,
        'dropout_rate': args.dropout_rate,
        'dataset_path': args.dataset_path,
        'processed_path': args.processed_path,
        'checkpoint_dir': args.checkpoint_dir,
        'log_dir': args.log_dir,
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    }
    return config


def train_model(config: Dict) -> Tuple[UVPFLModel, Dict]:
    """
    Train the UVPFL model.
    
    Args:
        config: Training configuration
        
    Returns:
        Tuple of (trained_model, training_history)
    """
    print("\n" + "=" * 60)
    print("UVPFL Training Pipeline")
    print("=" * 60)
    print(f"Model: {config['model_type']}")
    print(f"Epochs: {config['epochs']}")
    print(f"Batch size: {config['batch_size']}")
    print(f"Learning rate: {config['learning_rate']}")
    print(f"Backbone frozen: {config['freeze_backbone']}")
    print("=" * 60)
    
    # Create directories
    Path(config['checkpoint_dir']).mkdir(parents=True, exist_ok=True)
    Path(config['log_dir']).mkdir(parents=True, exist_ok=True)
    
    # Save config
    config_path = Path(config['checkpoint_dir']) / f"config_{config['timestamp']}.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\nConfig saved to: {config_path}")
    
    # Initialize data loader
    print("\nInitializing data loader...")
    data_loader = UVPFLDataLoaderFast(
        dataset_path=config['dataset_path'],
        processed_path=config['processed_path'],
        batch_size=config['batch_size']
    )
    
    # Get steps per epoch
    train_steps = data_loader.get_steps_per_epoch('train')
    val_steps = data_loader.get_steps_per_epoch('test')
    
    print(f"Train steps per epoch: {train_steps}")
    print(f"Validation steps: {val_steps}")
    
    # Limit steps for faster epochs (optional - for testing)
    # Can be removed for full training
    max_train_steps = min(train_steps, 1000)  # Limit for reasonable training time
    max_val_steps = min(val_steps, 200)
    
    print(f"Using {max_train_steps} train steps, {max_val_steps} val steps per epoch")
    
    # Initialize model
    print("\nInitializing model...")
    model = UVPFLModel(
        model_type=config['model_type'],
        sequence_length=config['sequence_length'],
        frame_height=config['frame_height'],
        frame_width=config['frame_width'],
        gru_units=config['gru_units'],
        dropout_rate=config['dropout_rate'],
        freeze_backbone=config['freeze_backbone'],
        learning_rate=config['learning_rate']
    )
    
    # Print model summary
    print("\nModel Summary:")
    model.summary()
    
    # Get callbacks
    callbacks = get_callbacks(
        model_name=f"uvpfl_{config['model_type']}_{config['timestamp']}",
        checkpoint_dir=config['checkpoint_dir'],
        log_dir=config['log_dir'],
        patience=10
    )
    
    # Create data generators
    train_gen = data_loader.train_generator(shuffle=True)
    val_gen = data_loader.test_generator()
    
    # Train the model
    print("\n" + "=" * 60)
    print("Starting Training...")
    print("=" * 60)
    
    history = model.model.fit(
        train_gen,
        steps_per_epoch=max_train_steps,
        epochs=config['epochs'],
        validation_data=val_gen,
        validation_steps=max_val_steps,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    final_model_path = Path(config['checkpoint_dir']) / f"uvpfl_{config['model_type']}_final.keras"
    model.save(str(final_model_path))
    print(f"\nFinal model saved to: {final_model_path}")
    
    # Save training history
    history_path = Path(config['log_dir']) / f"history_{config['timestamp']}.json"
    history_dict = {
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history.get('val_loss', [])],
        'mae': [float(x) for x in history.history.get('mae', [])],
        'val_mae': [float(x) for x in history.history.get('val_mae', [])],
    }
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    print(f"Training history saved to: {history_path}")
    
    return model, history_dict


def evaluate_model(model: UVPFLModel, data_loader: UVPFLDataLoaderFast, 
                   num_steps: int = 100) -> Dict:
    """
    Evaluate the trained model.
    
    Args:
        model: Trained UVPFL model
        data_loader: Data loader
        num_steps: Number of evaluation steps
        
    Returns:
        Dictionary with evaluation metrics
    """
    print("\n" + "=" * 60)
    print("Evaluating Model...")
    print("=" * 60)
    
    test_gen = data_loader.test_generator()
    
    results = model.model.evaluate(
        test_gen,
        steps=num_steps,
        return_dict=True,
        verbose=1
    )
    
    print(f"\nEvaluation Results:")
    for metric, value in results.items():
        print(f"  {metric}: {value:.4f}")
    
    return results


def quick_train(epochs: int = 5, batch_size: int = 4):
    """
    Quick training for testing the pipeline.
    
    Args:
        epochs: Number of epochs
        batch_size: Batch size
    """
    print("\n" + "=" * 60)
    print("Quick Training Mode (for testing)")
    print("=" * 60)
    
    # Create config
    config = {
        'model_type': 'resnet50',
        'batch_size': batch_size,
        'epochs': epochs,
        'learning_rate': 0.001,
        'sequence_length': SEQUENCE_LENGTH,
        'frame_height': FRAME_HEIGHT,
        'frame_width': FRAME_WIDTH,
        'channels': CHANNELS,
        'freeze_backbone': True,
        'gru_units': 128,
        'dropout_rate': 0.3,
        'dataset_path': '360dataset',
        'processed_path': 'processed_data',
        'checkpoint_dir': 'checkpoints',
        'log_dir': 'logs',
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    }
    
    # Initialize data loader
    print("\nInitializing data loader...")
    data_loader = UVPFLDataLoaderFast(
        dataset_path=config['dataset_path'],
        processed_path=config['processed_path'],
        batch_size=config['batch_size']
    )
    
    # Initialize model
    print("\nInitializing model...")
    model = UVPFLModel(
        model_type=config['model_type'],
        freeze_backbone=config['freeze_backbone'],
        learning_rate=config['learning_rate']
    )
    
    # Quick train with limited steps
    print("\nTraining...")
    train_gen = data_loader.train_generator(shuffle=True)
    val_gen = data_loader.test_generator()
    
    # Create checkpoint directory
    Path(config['checkpoint_dir']).mkdir(parents=True, exist_ok=True)
    
    history = model.model.fit(
        train_gen,
        steps_per_epoch=50,  # Very limited for quick test
        epochs=epochs,
        validation_data=val_gen,
        validation_steps=20,
        verbose=1
    )
    
    # Evaluate
    print("\nQuick evaluation...")
    test_gen = data_loader.test_generator()
    results = model.model.evaluate(test_gen, steps=20, return_dict=True, verbose=1)
    
    print(f"\nQuick Training Results:")
    print(f"  Final train loss: {history.history['loss'][-1]:.4f}")
    print(f"  Final val loss: {history.history.get('val_loss', [0])[-1]:.4f}")
    print(f"  Test loss: {results.get('loss', 0):.4f}")
    
    return model, history


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='UVPFL Training Pipeline')
    
    # Model settings
    parser.add_argument('--model_type', type=str, default='resnet50',
                        choices=['resnet50', 'mobilenet', 'lightweight'],
                        help='Model architecture (default: resnet50)')
    parser.add_argument('--gru_units', type=int, default=128,
                        help='Number of GRU units (default: 128)')
    parser.add_argument('--dropout_rate', type=float, default=0.3,
                        help='Dropout rate (default: 0.3)')
    parser.add_argument('--unfreeze_backbone', action='store_true',
                        help='Unfreeze backbone for fine-tuning')
    
    # Training settings
    parser.add_argument('--epochs', type=int, default=EPOCHS,
                        help=f'Number of epochs (default: {EPOCHS})')
    parser.add_argument('--batch_size', type=int, default=BATCH_SIZE,
                        help=f'Batch size (default: {BATCH_SIZE})')
    parser.add_argument('--learning_rate', type=float, default=LEARNING_RATE,
                        help=f'Learning rate (default: {LEARNING_RATE})')
    
    # Data settings
    parser.add_argument('--dataset_path', type=str, default='360dataset',
                        help='Path to dataset')
    parser.add_argument('--processed_path', type=str, default='processed_data',
                        help='Path to processed data')
    
    # Output settings
    parser.add_argument('--checkpoint_dir', type=str, default='checkpoints',
                        help='Checkpoint directory')
    parser.add_argument('--log_dir', type=str, default='logs',
                        help='Log directory')
    
    # Mode
    parser.add_argument('--quick', action='store_true',
                        help='Quick training mode for testing')
    parser.add_argument('--quick_epochs', type=int, default=5,
                        help='Epochs for quick training (default: 5)')
    
    args = parser.parse_args()
    
    # Print GPU info
    print_gpu_info()
    
    if args.quick:
        # Quick training for testing
        model, history = quick_train(epochs=args.quick_epochs, batch_size=args.batch_size)
    else:
        # Full training
        config = create_training_config(args)
        model, history = train_model(config)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()

