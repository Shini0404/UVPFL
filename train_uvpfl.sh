#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu
#SBATCH --job-name=uvpfl_train
#SBATCH --error=uvpfl_%j.err
#SBATCH --output=uvpfl_%j.out
#SBATCH --time=24:00:00
#SBATCH --mail-type=end
ulimit -s unlimited

# ============================================================
# UVPFL Training Job Script for Paramshivay Supercomputer
# ============================================================
# 
# Usage:
#   1. Edit paths below (MODIFY THESE!)
#   2. Submit: sbatch train_uvpfl.sh
#   3. Check: squeue -u $USER
#   4. View output: tail -f uvpfl_<jobid>.out
#
# ============================================================

# ============================================================
# MODIFY THESE PATHS FOR YOUR SETUP
# ============================================================

# Path to your virtual environment
VENV_PATH="/home/shinikoushal.cse24.itbhu/Shini/UVPFL/uvpf_env"

# Path to UVPFL project directory
PROJECT_PATH="/home/shinikoushal.cse24.itbhu/Shini/UVPFL"

# CUDA version (Paramshivay specific)
CUDA_VERSION="12.6.3"  # Default on Paramshivay

# Python module (Paramshivay specific)
PYTHON_MODULE="miniconda_23.5.2_python_3.11.4"  # Python 3.11
# Alternative: "anaconda/3/python3.7" or "intelpython/3.6"

# ============================================================
# Load Required Modules
# ============================================================

echo "============================================================"
echo "Loading modules..."
echo "============================================================"

module load cuda/${CUDA_VERSION}
module load ${PYTHON_MODULE}
module load gcc/11.1.0
module load hdf5-1.12.0/mpich-gcc  # Required for h5py

echo "Loaded modules:"
module list

# ============================================================
# Activate Virtual Environment
# ============================================================

echo "============================================================"
echo "Activating virtual environment..."
echo "============================================================"

if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    echo "Please create it first: python3 -m venv $VENV_PATH"
    exit 1
fi

source ${VENV_PATH}/bin/activate

# ============================================================
# Set Working Directory
# ============================================================

cd ${PROJECT_PATH}

if [ ! -f "train.py" ]; then
    echo "ERROR: train.py not found in ${PROJECT_PATH}"
    echo "Please check your PROJECT_PATH"
    exit 1
fi

# ============================================================
# GPU Configuration
# ============================================================

export TF_FORCE_GPU_ALLOW_GROWTH=true
export CUDA_VISIBLE_DEVICES=0

# ============================================================
# Verify Environment
# ============================================================

echo "============================================================"
echo "Verifying environment..."
echo "============================================================"

python --version
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__); print('GPUs:', tf.config.list_physical_devices('GPU'))"

# ============================================================
# Run Training
# ============================================================

echo "============================================================"
echo "Starting UVPFL training..."
echo "============================================================"
echo "Start time: $(date)"
echo "============================================================"

# Full training (50 epochs, batch size 16 for 16GB GPU)
python train.py --epochs 50 --batch_size 16

# Or run complete pipeline:
# python run_complete.py

echo "============================================================"
echo "Training completed!"
echo "End time: $(date)"
echo "============================================================"

