"""
GPU Memory Optimization for UVPFL

This script helps optimize batch size and training parameters for 8GB GPU.
The actual issue is GPU license, not memory - 8GB is sufficient!
"""

import tensorflow as tf
import numpy as np
from pathlib import Path


def calculate_memory_requirements(batch_size: int = 8):
    """
    Calculate memory requirements for UVPFL model.
    
    Args:
        batch_size: Batch size to calculate for
        
    Returns:
        Dictionary with memory breakdown
    """
    # Model parameters
    SEQUENCE_LENGTH = 30
    FRAME_HEIGHT = 120
    FRAME_WIDTH = 240
    CHANNELS = 3
    MODEL_PARAMS = 24_432_515
    
    # Memory calculations
    bytes_per_float = 4  # float32
    
    # Input data memory
    input_per_sample = SEQUENCE_LENGTH * FRAME_HEIGHT * FRAME_WIDTH * CHANNELS * bytes_per_float
    input_batch = input_per_sample * batch_size
    
    # Model memory (weights)
    model_memory = MODEL_PARAMS * bytes_per_float
    
    # Gradient memory (same as model)
    gradient_memory = model_memory
    
    # Activation memory (approximate)
    # ResNet50 output: batch * sequence * features
    resnet_features = 2048
    activation_memory = batch_size * SEQUENCE_LENGTH * resnet_features * bytes_per_float
    
    # GRU memory (approximate)
    gru_units = 128
    gru_memory = batch_size * SEQUENCE_LENGTH * gru_units * bytes_per_float
    
    # Total
    total_memory = (
        input_batch +
        model_memory +
        gradient_memory +
        activation_memory +
        gru_memory
    )
    
    # Add 30% overhead for safety
    total_with_overhead = total_memory * 1.3
    
    # 8GB GPU = 8192 MB, but ~6000 MB usable (after system overhead)
    fits_in_8gb = total_with_overhead < 6000
    
    return {
        'batch_size': batch_size,
        'input_memory_mb': input_batch / (1024**2),
        'model_memory_mb': model_memory / (1024**2),
        'gradient_memory_mb': gradient_memory / (1024**2),
        'activation_memory_mb': activation_memory / (1024**2),
        'gru_memory_mb': gru_memory / (1024**2),
        'total_memory_mb': total_memory / (1024**2),
        'total_with_overhead_mb': total_with_overhead / (1024**2),
        'fits_in_8gb': fits_in_8gb,
        'utilization_percent': (total_with_overhead / 6000) * 100
    }


def find_optimal_batch_size(max_memory_mb: int = 6000):
    """
    Find optimal batch size for given memory limit.
    
    Args:
        max_memory_mb: Maximum memory in MB (default: 6000 for 8GB GPU)
        
    Returns:
        Optimal batch size
    """
    for batch_size in [16, 12, 8, 6, 4, 2, 1]:
        mem = calculate_memory_requirements(batch_size)
        if mem['total_with_overhead_mb'] < max_memory_mb:
            return batch_size, mem
    
    return 1, calculate_memory_requirements(1)


def print_memory_analysis():
    """Print detailed memory analysis."""
    print("=" * 60)
    print("UVPFL GPU Memory Analysis")
    print("=" * 60)
    
    print("\n⚠️  IMPORTANT: The error you're seeing is NOT a memory issue!")
    print("   It's a GPU LICENSE issue (Grid license).")
    print("   8GB GPU is MORE than enough for this model!")
    print("=" * 60)
    
    print("\n📊 Memory Requirements for Different Batch Sizes:\n")
    
    for batch_size in [16, 12, 8, 6, 4, 2, 1]:
        mem = calculate_memory_requirements(batch_size)
        utilization = (mem['total_with_overhead_mb'] / 6000) * 100  # 6000 MB usable
        # All batch sizes up to 16 fit easily (use < 8% of memory)
        status = "✅ Fits" if utilization < 10 else "⚠️  Check"
        
        print(f"Batch Size {batch_size:2d}:")
        print(f"  Input:        {mem['input_memory_mb']:6.1f} MB")
        print(f"  Model:        {mem['model_memory_mb']:6.1f} MB")
        print(f"  Gradients:    {mem['gradient_memory_mb']:6.1f} MB")
        print(f"  Activations:  {mem['activation_memory_mb']:6.1f} MB")
        print(f"  GRU:          {mem['gru_memory_mb']:6.1f} MB")
        print(f"  Total:        {mem['total_with_overhead_mb']:6.1f} MB ({utilization:.1f}% of 6GB usable) {status}")
        print()
    
    # Find optimal
    optimal_batch, optimal_mem = find_optimal_batch_size()
    print(f"\n✅ Recommended batch size: {optimal_batch}")
    print(f"   Uses: {optimal_mem['total_with_overhead_mb']:.1f} MB / 6000 MB available")
    print(f"   Safety margin: {(6000 - optimal_mem['total_with_overhead_mb']) / 6000 * 100:.1f}%")
    
    print("\n" + "=" * 60)
    print("💡 Solutions:")
    print("=" * 60)
    print("1. Use CPU (if GPU license issue):")
    print("   python3 run_complete.py --use_cpu")
    print()
    print("2. Use smaller batch size (if memory issue):")
    print("   python3 train.py --batch_size 4")
    print()
    print("3. Use MobileNet (lighter model):")
    print("   python3 train.py --model_type mobilenet --batch_size 8")
    print()
    print("4. Use gradient checkpointing (saves memory):")
    print("   (Already implemented in model)")
    print("=" * 60)


def create_optimized_training_config():
    """Create optimized training configuration for 8GB GPU."""
    config = {
        'batch_size_8gb': {
            'batch_size': 8,
            'gradient_accumulation': 1,
            'mixed_precision': False,
            'estimated_memory_mb': calculate_memory_requirements(8)['total_with_overhead_mb']
        },
        'batch_size_4gb': {
            'batch_size': 4,
            'gradient_accumulation': 2,  # Effective batch size 8
            'mixed_precision': False,
            'estimated_memory_mb': calculate_memory_requirements(4)['total_with_overhead_mb']
        },
        'batch_size_2gb': {
            'batch_size': 2,
            'gradient_accumulation': 4,  # Effective batch size 8
            'mixed_precision': True,  # Use mixed precision
            'estimated_memory_mb': calculate_memory_requirements(2)['total_with_overhead_mb']
        }
    }
    
    return config


if __name__ == '__main__':
    print_memory_analysis()
    
    print("\n📋 Optimized Training Configurations:\n")
    configs = create_optimized_training_config()
    for name, config in configs.items():
        print(f"{name}:")
        print(f"  Batch size: {config['batch_size']}")
        print(f"  Gradient accumulation: {config['gradient_accumulation']}")
        print(f"  Mixed precision: {config['mixed_precision']}")
        print(f"  Memory: {config['estimated_memory_mb']:.1f} MB")
        print()

