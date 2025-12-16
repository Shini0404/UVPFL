#!/bin/bash
#SBATCH --job-name=uvpfl_test
#SBATCH --output=test_%j.out
#SBATCH --error=test_%j.err
#SBATCH --gres=gpu:1
#SBATCH --time=0:30:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4

# ============================================================
# UVPFL GPU Test Script for Paramshivay
# ============================================================
# Quick test to verify GPU access and environment
# Usage: sbatch test_gpu.sh
# ============================================================

# MODIFY THESE PATHS
VENV_PATH="$WORK/uvpf_env"  # CHANGE THIS!
PROJECT_PATH="$WORK/UVPFL"   # CHANGE THIS!

# Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load hdf5-1.12.0/mpich-gcc  # Required for h5py

# Activate environment
source ${VENV_PATH}/bin/activate

# Navigate to project
cd ${PROJECT_PATH}

# Test GPU
echo "============================================================"
echo "Testing GPU Access"
echo "============================================================"

echo "1. Checking nvidia-smi..."
nvidia-smi

echo ""
echo "2. Checking TensorFlow GPU..."
python -c "
import tensorflow as tf
print('TensorFlow version:', tf.__version__)
print('CUDA built:', tf.test.is_built_with_cuda())
gpus = tf.config.list_physical_devices('GPU')
print('GPUs found:', len(gpus))
for gpu in gpus:
    print('  -', gpu)
"

echo ""
echo "3. Running environment verification..."
python verify_environment.py

echo ""
echo "4. Testing model creation..."
python -c "
from model import UVPFLModel
import numpy as np
print('Creating model...')
model = UVPFLModel()
print('✅ Model created successfully!')
dummy = np.random.rand(1, 30, 120, 240, 3).astype(np.float32)
print('Testing forward pass...')
output = model.predict(dummy)
print(f'✅ Forward pass works! Output shape: {output.shape}')
"

echo ""
echo "============================================================"
echo "✅ All tests passed! GPU is ready for training."
echo "============================================================"

