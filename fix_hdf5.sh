#!/bin/bash
# Quick fix script for HDF5 error on Paramshivay

echo "============================================================"
echo "Fixing HDF5 Error for TensorFlow Installation"
echo "============================================================"

# Load required modules
echo "1. Loading modules..."
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0
module load hdf5-1.12.0/mpich-gcc

# Activate environment
echo "2. Activating environment..."
source uvpf_env/bin/activate

# Set HDF5 paths
echo "3. Setting HDF5 environment variables..."
export HDF5_DIR=$(dirname $(dirname $(which h5cc))) 2>/dev/null
if [ -z "$HDF5_DIR" ]; then
    echo "   Warning: h5cc not found, trying module path..."
    export HDF5_DIR=/opt/ohpc/pub/libs/gnu8/mpich/hdf5/1.12.0 2>/dev/null
fi
export HDF5_INCLUDE_DIR=$HDF5_DIR/include 2>/dev/null
export HDF5_LIB_DIR=$HDF5_DIR/lib 2>/dev/null
export LD_LIBRARY_PATH=$HDF5_LIB_DIR:$LD_LIBRARY_PATH

echo "   HDF5_DIR: $HDF5_DIR"

# Install h5py (pre-built)
echo "4. Installing h5py (pre-built wheel)..."
pip install --only-binary=h5py h5py

# Install TensorFlow
echo "5. Installing TensorFlow..."
pip install tensorflow[and-cuda]>=2.15.0

# Install other requirements
echo "6. Installing other requirements..."
pip install -r requirements.txt

echo ""
echo "============================================================"
echo "✅ Installation complete!"
echo "============================================================"
echo ""
echo "Verify installation:"
echo "  python -c 'import tensorflow as tf; print(\"TensorFlow:\", tf.__version__)'"
echo "  python -c 'import h5py; print(\"h5py:\", h5py.__version__)'"
