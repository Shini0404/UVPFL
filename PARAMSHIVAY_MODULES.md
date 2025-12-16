# Paramshivay Module Reference

Quick reference for available modules on Paramshivay supercomputer.

## ✅ Recommended Modules for UVPFL

### CUDA
```bash
module load cuda/12.6.3  # Default (recommended)
# Alternatives: cuda/11.1, cuda/10.1, cuda/9.2
```

### Python
```bash
# Option 1: Miniconda Python 3.11 (RECOMMENDED)
module load miniconda_23.5.2_python_3.11.4

# Option 2: Anaconda Python 3.7
module load anaconda/3/python3.7

# Option 3: Intel Python 3.6 (default)
module load intelpython/3.6
```

### GCC
```bash
module load gcc/11.1.0  # Default (recommended)
# Alternatives: gcc/10.2.0, gcc/9.2.0, gcc/7.5.0
```

---

## 📋 All Available Modules (from `module avail`)

### CUDA Modules
- `cuda/12.6.3` (D) - **Default, recommended**
- `cuda/11.1`
- `cuda/10.1`
- `cuda/10.0`
- `cuda/9.2`
- `cuda/9.0`
- `cuda/8.0`
- `cuda/7.0`

### Python Modules
- `miniconda_23.5.2_python_3.11.4` - **Recommended (Python 3.11)**
- `anaconda/3/python3.7` - Python 3.7
- `python3.8/3.8` - Python 3.8
- `python3.7/3.7` - Python 3.7
- `python3.6/3.6` - Python 3.6
- `intelpython/3.6` (D) - Intel Python 3.6 (default)
- `conda/4.8.3`
- `conda-python/3.7`

### GCC Modules
- `gcc/11.1.0` (D) - **Default, recommended**
- `gcc/10.2.0`
- `gcc/9.2.0`
- `gcc/7.5.0`
- `gcc/6.5.0`
- `gcc/5.5.0`

### TensorFlow Modules (OLD - Don't Use)
- `tensorflow/gpu-1.12.0-with-python3.6` (D) - **Too old!**
- `tensorflow/cpu-1.12.0-with-python3.6`
- `tensorflow-intel/1.13.1_with_python3.6` (D) - **Too old!**

**Note:** Paramshivay's TensorFlow modules are version 1.12-1.13 (from 2018-2019). We need TensorFlow 2.15+ (2024), so we'll install it manually in a virtual environment.

---

## 🎯 Complete Setup Command

```bash
# Load recommended modules
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0

# Create environment
python -m venv uvpf_env
source uvpf_env/bin/activate

# Install TensorFlow 2.15+ with GPU
pip install --upgrade pip
pip install tensorflow[and-cuda]>=2.15.0
pip install -r requirements.txt
```

---

## 🔍 Finding Modules

```bash
# List all available modules
module avail

# Search for specific module
module keyword cuda
module keyword python
module keyword gcc

# Get detailed info about a module
module spider cuda
module spider python
```

---

## ⚠️ Important Notes

1. **CUDA 12.6.3** is the default and latest available
2. **Miniconda Python 3.11** is recommended (newest Python)
3. **TensorFlow modules are outdated** - install TensorFlow 2.15+ manually
4. **GCC 11.1.0** is default and sufficient
5. Always check module compatibility before loading

---

## 📝 Module Loading Order

```bash
# 1. Load CUDA first
module load cuda/12.6.3

# 2. Load Python
module load miniconda_23.5.2_python_3.11.4

# 3. Load GCC (if needed for compilation)
module load gcc/11.1.0

# 4. Verify
module list
```

---

## 🚨 Common Issues

### Issue: Module not found
```bash
# Check exact name
module avail | grep -i cuda
module avail | grep -i python
```

### Issue: Python version mismatch
```bash
# Use miniconda for Python 3.11
module load miniconda_23.5.2_python_3.11.4
python --version  # Should show 3.11.x
```

### Issue: CUDA version mismatch
```bash
# Use default CUDA 12.6.3
module load cuda/12.6.3
nvcc --version  # Verify CUDA version
```

---

**Last Updated:** Based on Paramshivay `module avail` output

