# Fix HDF5 Error on Paramshivay

## 🚨 Error You're Seeing

```
error: Unable to load dependency HDF5, make sure HDF5 is installed properly
error: libhdf5.so: cannot open shared object file: No such file or directory
```

**Cause:** h5py (used by TensorFlow) needs HDF5 libraries, but they're not loaded.

---

## ✅ Solution

### **Step 1: Load HDF5 Module**

```bash
# Load HDF5 module (choose one that works)
module load hdf5-1.12.0/mpich-gcc
# OR
module load hdf5-1.14.2-intel2020
# OR
module load hdf5/1.10.0-patch1/intel

# Verify it's loaded
module list | grep hdf5
```

### **Step 2: Set HDF5 Environment Variables**

```bash
# Find HDF5 location
which h5cc  # Should show path if HDF5 is loaded

# Set environment variables
export HDF5_DIR=$(dirname $(dirname $(which h5cc)))
export HDF5_INCLUDE_DIR=$HDF5_DIR/include
export HDF5_LIB_DIR=$HDF5_DIR/lib

# Verify
echo $HDF5_DIR
```

### **Step 3: Install h5py (Pre-built Wheel - Recommended)**

```bash
# Install pre-built h5py (avoids compilation)
pip install --only-binary=h5py h5py

# Then install TensorFlow
pip install tensorflow[and-cuda]>=2.15.0
```

---

## 🎯 Complete Fix (Copy-Paste)

```bash
# 1. Load all required modules
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0
module load hdf5-1.12.0/mpich-gcc

# 2. Activate environment
source uvpf_env/bin/activate

# 3. Set HDF5 paths (if h5cc is available)
export HDF5_DIR=$(dirname $(dirname $(which h5cc))) 2>/dev/null
export HDF5_INCLUDE_DIR=$HDF5_DIR/include 2>/dev/null
export HDF5_LIB_DIR=$HDF5_DIR/lib 2>/dev/null

# 4. Install h5py (pre-built, no compilation)
pip install --only-binary=h5py h5py

# 5. Install TensorFlow
pip install tensorflow[and-cuda]>=2.15.0

# 6. Install other requirements
pip install -r requirements.txt
```

---

## 🔧 Alternative: If Pre-built h5py Doesn't Work

### **Option 1: Install h5py with HDF5 from Module**

```bash
# Load HDF5
module load hdf5-1.12.0/mpich-gcc

# Find HDF5 paths
module show hdf5-1.12.0/mpich-gcc

# Set paths manually (adjust based on module show output)
export HDF5_DIR=/path/to/hdf5  # From module show
export HDF5_INCLUDE_DIR=$HDF5_DIR/include
export HDF5_LIB_DIR=$HDF5_DIR/lib
export LD_LIBRARY_PATH=$HDF5_LIB_DIR:$LD_LIBRARY_PATH

# Install h5py
pip install h5py
```

### **Option 2: Use Conda (If Available)**

```bash
# If conda is available
conda install -c conda-forge h5py
pip install tensorflow[and-cuda]>=2.15.0
```

### **Option 3: Skip h5py for Now**

```bash
# Install TensorFlow without h5py (some features may be limited)
pip install tensorflow[and-cuda]>=2.15.0 --no-deps
pip install numpy pandas scipy opencv-python Pillow scikit-learn matplotlib seaborn tqdm
# h5py will be installed later if needed
```

---

## 📋 Available HDF5 Modules on Paramshivay

From `module avail`:
- `hdf5-1.12.0/mpich-gcc` ⭐ **Recommended**
- `hdf5-1.14.2-intel2020`
- `hdf5/1.10.0-patch1/intel`
- `hdf5-1.10.0/mpich-gcc/1.10.0`
- `parallel_hdf5_1.8.21`

---

## ✅ Verify Installation

```bash
# Check h5py
python -c "import h5py; print('h5py version:', h5py.__version__)"

# Check TensorFlow
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
```

---

## 🚨 If Still Failing

1. **Check HDF5 module:**
   ```bash
   module show hdf5-1.12.0/mpich-gcc
   ```

2. **Check library path:**
   ```bash
   ldconfig -p | grep hdf5
   ```

3. **Try different HDF5 module:**
   ```bash
   module unload hdf5-1.12.0/mpich-gcc
   module load hdf5-1.14.2-intel2020
   ```

4. **Contact Paramshivay support** if none work.

---

**Quick Fix:** Just run the "Complete Fix" commands above! 🚀

