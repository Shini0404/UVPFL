# Paramshivay Supercomputer Setup Guide

Complete guide for setting up UVPFL on Paramshivay supercomputer with 16GB GPU.

---

## 🎯 Overview

**Paramshivay Supercomputer:**
- GPU: 16GB (NVIDIA, likely V100 or A100)
- System: Linux-based HPC cluster
- Job Scheduler: SLURM (typical for supercomputers)
- Module System: Environment Modules (typical)

**What We Need:**
- Python 3.8+
- CUDA 11.8+ or 12.0+
- TensorFlow with GPU support
- All dependencies from `requirements.txt`

---

## 📋 Step-by-Step Setup

### **STEP 1: Login to Paramshivay**

```bash
# SSH to Paramshivay
ssh username@paramshivay.hpc.institute.edu  # Replace with actual hostname
# Or
ssh username@login.paramshivay.institute.edu
```

---

### **STEP 2: Check Available Modules**

```bash
# Check available modules
module avail

# Check GPU modules
module avail cuda
module avail python
module avail gcc

# Check GPU availability
nvidia-smi
```

**Expected output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 5xx.xx       Driver Version: 5xx.xx       CUDA Version: 12.x   |
+-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Purb  P|:N/A|     P|:N/A      P|:N/A |                  N/A |
|===============================+======================+======================|
|   0  NVIDIA V100 ...    Off  | 00000000:XX:00.0 Off |                    0 |
| N/A   XX°C    P0    XXW / XXXW |   XXXXXMiB / 16384MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

---

### **STEP 3: Load Required Modules**

**Based on Paramshivay's available modules:**

```bash
# Load CUDA (default is 12.6.3)
module load cuda/12.6.3  # Default, or use: cuda/11.1, cuda/10.1, cuda/9.2

# Load Python (choose one)
# Option 1: Miniconda with Python 3.11 (RECOMMENDED)
module load miniconda_23.5.2_python_3.11.4

# Option 2: Anaconda with Python 3.7
# module load anaconda/3/python3.7

# Option 3: Intel Python 3.6 (default)
# module load intelpython/3.6

# Load GCC (default is 11.1.0)
module load gcc/11.1.0  # Default, or use: gcc/10.2.0, gcc/9.2.0

# Verify loaded modules
module list
```

**Paramshivay Available Modules:**
- **CUDA:** `cuda/12.6.3` (default), `cuda/11.1`, `cuda/10.1`, `cuda/9.2`, `cuda/9.0`, `cuda/8.0`
- **Python:** `miniconda_23.5.2_python_3.11.4`, `anaconda/3/python3.7`, `python3.8/3.8`, `python3.7/3.7`, `intelpython/3.6` (default)
- **GCC:** `gcc/11.1.0` (default), `gcc/10.2.0`, `gcc/9.2.0`, `gcc/7.5.0`, `gcc/6.5.0`

**Note:** TensorFlow modules on Paramshivay are old (1.12.0, 1.13.1). We'll install TensorFlow 2.15+ manually.

---

### **STEP 4: Create Python Virtual Environment**

```bash
# Navigate to your work directory
cd $WORK  # or $HOME, or your project directory
# OR
cd /path/to/your/project

# After loading Python module, create virtual environment
# If using miniconda:
python -m venv uvpf_env

# If using anaconda/intelpython:
python3 -m venv uvpf_env

# Activate virtual environment
source uvpf_env/bin/activate

# Verify Python version
python --version  # Should be 3.8+ (3.11 if using miniconda)
```

---

### **STEP 5: Load HDF5 Module (Required for h5py)**

```bash
# h5py (used by TensorFlow) requires HDF5 libraries
# Load HDF5 module before installing TensorFlow
module load hdf5-1.12.0/mpich-gcc
# OR try: module load hdf5-1.14.2-intel2020
# OR: module load hdf5/1.10.0-patch1/intel

# Verify HDF5 is loaded
module list | grep hdf5
```

**Available HDF5 modules on Paramshivay:**
- `hdf5-1.12.0/mpich-gcc` (recommended)
- `hdf5-1.14.2-intel2020`
- `hdf5/1.10.0-patch1/intel`
- `hdf5-1.10.0/mpich-gcc/1.10.0`

---

### **STEP 6: Install CUDA-Enabled TensorFlow**

```bash
# Make sure you're in the virtual environment
source uvpf_env/bin/activate

# Make sure HDF5 module is loaded (from Step 5)
module load hdf5-1.12.0/mpich-gcc

# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Set environment variables for HDF5
export HDF5_DIR=$(dirname $(dirname $(which h5cc)))
export HDF5_INCLUDE_DIR=$HDF5_DIR/include
export HDF5_LIB_DIR=$HDF5_DIR/lib

# Install TensorFlow with CUDA support
# Option 1: TensorFlow 2.15+ (recommended)
pip install tensorflow[and-cuda]>=2.15.0

# Option 2: If Option 1 doesn't work, install separately
pip install tensorflow>=2.15.0
pip install nvidia-cudnn-cu11  # or nvidia-cudnn-cu12

# Verify TensorFlow can see GPU
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__); print('GPUs:', tf.config.list_physical_devices('GPU'))"
```

**If h5py still fails, try installing pre-built h5py:**
```bash
# Install h5py from pre-built wheel (avoids compilation)
pip install --only-binary=h5py h5py
pip install tensorflow[and-cuda]>=2.15.0
```

**Expected output:**
```
TensorFlow: 2.15.0
GPUs: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

---

### **STEP 6: Install All Dependencies**

```bash
# Make sure you're in virtual environment
source uvpf_env/bin/activate

# Navigate to UVPFL directory
cd /path/to/UVPFL  # Replace with your actual path

# Install all requirements
pip install -r requirements.txt

# If pip install fails, install individually:
pip install numpy>=1.23.0
pip install pandas>=1.5.0
pip install scipy>=1.9.0
pip install opencv-python>=4.6.0
pip install Pillow>=9.0.0
pip install scikit-learn>=1.1.0
pip install matplotlib>=3.6.0
pip install seaborn>=0.12.0
pip install tqdm>=4.64.0
pip install jupyter>=1.0.0
pip install ipykernel>=6.0.0
```

---

### **STEP 7: Verify Environment**

```bash
# Make sure you're in virtual environment
source uvpf_env/bin/activate

# Navigate to UVPFL directory
cd /path/to/UVPFL

# Run verification script
python verify_environment.py
```

**Expected output:**
```
============================================================
UVPFL Environment Verification
============================================================
✅ TensorFlow: 2.15.0
✅ GPU Available: 1 device(s)
   - /physical_device:GPU:0
✅ Keras: 2.15.0
✅ NumPy: 1.24.0
✅ Pandas: 2.0.0
✅ OpenCV: 4.8.0
✅ All dependencies installed!
============================================================
```

---

### **STEP 8: Transfer Your Code and Dataset**

**Option A: Using SCP (from your local machine):**

```bash
# From your local machine
scp -r /home/arunabha/Shini/UVPFL username@paramshivay:/path/to/destination/

# Transfer dataset separately (if large)
scp -r /home/arunabha/Shini/UVPFL/360dataset username@paramshivay:/path/to/UVPFL/
```

**Option B: Using Git (if code is in repository):**

```bash
# On Paramshivay
cd $WORK
git clone <your-repo-url>
cd UVPFL
```

**Option C: Using rsync (efficient for large files):**

```bash
# From your local machine
rsync -avz --progress /home/arunabha/Shini/UVPFL/ username@paramshivay:/path/to/UVPFL/
```

---

## 🚀 Running Jobs on Paramshivay

### **Method 1: Interactive GPU Session (For Testing)**

```bash
# Request interactive GPU session
srun --gres=gpu:1 --time=2:00:00 --mem=16G --pty bash

# Once you get the session:
source uvpf_env/bin/activate
cd /path/to/UVPFL
python run_complete.py
```

**SLURM parameters:**
- `--gres=gpu:1`: Request 1 GPU
- `--time=2:00:00`: 2 hours time limit
- `--mem=16G`: 16GB RAM
- `--pty bash`: Interactive bash shell

---

### **Method 2: Submit Job Script (For Training)**

Create a job script `train_uvpfl.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=uvpfl_train
#SBATCH --output=uvpfl_%j.out
#SBATCH --error=uvpfl_%j.err
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --partition=gpu  # Adjust partition name as needed

# Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0

# Activate virtual environment
source /path/to/uvpf_env/bin/activate

# Set working directory
cd /path/to/UVPFL

# Set GPU memory growth
export TF_FORCE_GPU_ALLOW_GROWTH=true

# Run training
python train.py --epochs 50 --batch_size 16

# Or run complete pipeline
# python run_complete.py
```

**Submit the job:**

```bash
sbatch train_uvpfl.sh
```

**Check job status:**

```bash
squeue -u $USER
```

**View output:**

```bash
tail -f uvpfl_<jobid>.out
```

---

### **Method 3: Quick Test Script**

Create `test_gpu.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=uvpfl_test
#SBATCH --output=test_%j.out
#SBATCH --error=test_%j.err
#SBATCH --gres=gpu:1
#SBATCH --time=0:30:00
#SBATCH --mem=16G

module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4

source /path/to/uvpf_env/bin/activate
cd /path/to/UVPFL

python verify_environment.py
python -c "import tensorflow as tf; print('GPU:', tf.config.list_physical_devices('GPU'))"
```

---

## 🔧 Common Issues and Solutions

### **Issue 1: Module Not Found**

```bash
# Check available modules
module avail

# Try different module names
module load cuda
module load python
module load gcc
```

### **Issue 2: TensorFlow Can't See GPU**

```bash
# Check CUDA version
nvcc --version

# Check GPU
nvidia-smi

# Verify CUDA in Python
python -c "import tensorflow as tf; print(tf.test.is_built_with_cuda())"
# Should print: True

# Check CUDA libraries
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

**Solution:**
- Make sure CUDA module is loaded: `module load cuda/12.6.3`
- Install matching TensorFlow version
- Check CUDA compatibility: TensorFlow 2.15 works with CUDA 12.6.3 (Paramshivay default)

### **Issue 3: Out of Memory (OOM)**

**For 16GB GPU, you can use larger batches:**

```bash
# In train.py or run_complete.py
python train.py --batch_size 16  # Safe for 16GB GPU
python train.py --batch_size 32  # May work, test first
```

**Or set memory growth:**

```python
# In your script, before importing TensorFlow
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
```

### **Issue 4: Permission Denied**

```bash
# Make scripts executable
chmod +x train_uvpfl.sh
chmod +x test_gpu.sh
```

### **Issue 5: Virtual Environment Not Found**

```bash
# Recreate virtual environment
rm -rf uvpf_env
python3 -m venv uvpf_env
source uvpf_env/bin/activate
pip install -r requirements.txt
```

---

## 📊 Optimized Settings for 16GB GPU

### **Batch Size Recommendations:**

| Batch Size | Memory Usage | Status |
|------------|--------------|--------|
| 16 | ~700 MB | ✅ **Recommended** |
| 32 | ~1.2 GB | ✅ Safe |
| 64 | ~2.4 GB | ✅ Safe (if data fits) |

### **Training Command:**

```bash
# Full training with optimal settings
python train.py \
    --epochs 50 \
    --batch_size 16 \
    --learning_rate 0.001
```

---

## ✅ Complete Setup Checklist

- [ ] Logged into Paramshivay
- [ ] Loaded CUDA module (`module load cuda/12.6.3`)
- [ ] Loaded Python module (`module load miniconda_23.5.2_python_3.11.4`)
- [ ] Created virtual environment (`python3 -m venv uvpf_env`)
- [ ] Activated virtual environment (`source uvpf_env/bin/activate`)
- [ ] Installed TensorFlow with GPU (`pip install tensorflow[and-cuda]`)
- [ ] Installed all dependencies (`pip install -r requirements.txt`)
- [ ] Verified environment (`python verify_environment.py`)
- [ ] Transferred code and dataset to Paramshivay
- [ ] Tested GPU access (`python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"`)
- [ ] Created job script (`train_uvpfl.sh`)
- [ ] Submitted test job (`sbatch test_gpu.sh`)

---

## 🎯 Quick Start Commands

**One-time setup:**

```bash
# 1. Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0
module load hdf5-1.12.0/mpich-gcc  # Required for h5py

# 2. Create and activate environment
python -m venv uvpf_env
source uvpf_env/bin/activate

# 3. Set HDF5 environment variables
export HDF5_DIR=$(dirname $(dirname $(which h5cc))) 2>/dev/null || echo "HDF5 not in PATH, using module"
export HDF5_INCLUDE_DIR=$HDF5_DIR/include 2>/dev/null
export HDF5_LIB_DIR=$HDF5_DIR/lib 2>/dev/null

# 4. Install dependencies
pip install --upgrade pip
pip install --only-binary=h5py h5py  # Pre-built h5py (avoids compilation)
pip install tensorflow[and-cuda]>=2.15.0
pip install -r requirements.txt

# 5. Verify
python verify_environment.py
```

**Every time you login:**

```bash
# 1. Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4

# 2. Activate environment
source /path/to/uvpf_env/bin/activate

# 3. Navigate to project
cd /path/to/UVPFL

# 4. Run
python run_complete.py
```

---

## 📞 Getting Help

**If you encounter issues:**

1. **Check Paramshivay documentation:**
   - User guide
   - Module documentation
   - GPU allocation policies

2. **Contact Paramshivay support:**
   - Email: support@paramshivay.institute.edu (adjust as needed)
   - Check queue status: `squeue`
   - Check account limits: `sacctmgr show assoc user=$USER`

3. **Common commands:**
   ```bash
   # Check available GPUs
   sinfo -o "%N %G %m %t"
   
   # Check your jobs
   squeue -u $USER
   
   # Cancel job
   scancel <jobid>
   
   # Check job details
   scontrol show job <jobid>
   ```

---

## 🎉 Success Indicators

You're ready when:

1. ✅ `nvidia-smi` shows your GPU
2. ✅ `python verify_environment.py` shows GPU available
3. ✅ `python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"` shows GPU
4. ✅ Test job runs successfully

**Then you can run full training!**

---

## 📝 Notes

- **16GB GPU is MORE than enough** - You can use batch size 16-32 easily
- **Training time:** ~1-2 hours for 50 epochs (on 16GB GPU)
- **Storage:** Make sure you have enough space for:
  - Dataset: ~2 GB
  - Processed data: ~200 MB
  - Checkpoints: ~500 MB
  - Logs: ~100 MB
  - Total: ~3 GB

---

**Good luck with your training on Paramshivay! 🚀**

