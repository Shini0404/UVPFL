# Paramshivay Quick Start - One Page Reference

## 🚀 Setup (One Time)

# 1. Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
module load gcc/11.1.0

# 2. Create environment
python3 -m venv uvpf_env
source uvpf_env/bin/activate

# 3. Install
pip install --upgrade pip
pip install tensorflow[and-cuda]>=2.15.0
pip install -r requirements.txt

# 4. Verify
python verify_environment.py
```

---

## 📝 Every Login

# Load modules (Paramshivay specific)
module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4

# Activate environment
source $WORK/uvpf_env/bin/activate

# Go to project
cd $WORK/UVPFL
```

---

## 🎯 Run Training

### Option 1: Interactive Session
```bash
srun --gres=gpu:1 --time=2:00:00 --mem=16G --pty bash
source uvpf_env/bin/activate
cd $WORK/UVPFL
python run_complete.py
```

### Option 2: Submit Job
```bash
# Edit train_uvpfl.sh (change paths!)
sbatch train_uvpfl.sh

# Check status
squeue -u $USER

# View output
tail -f uvpfl_<jobid>.out
```

### Option 3: Quick Test
```bash
sbatch test_gpu.sh
```

---

## ⚙️ Job Script Template

```bash
#!/bin/bash
#SBATCH --job-name=uvpfl
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8

module load cuda/12.6.3
module load miniconda_23.5.2_python_3.11.4
source $WORK/uvpf_env/bin/activate
cd $WORK/UVPFL
python train.py --epochs 50 --batch_size 16
```

---

## ✅ Verify GPU

```bash
# Check GPU
nvidia-smi

# Check TensorFlow
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `module avail` to see available modules |
| GPU not visible | Check `module load cuda/12.6.3` |
| Import error | `pip install -r requirements.txt` |
| Out of memory | Reduce `--batch_size` (16GB GPU can handle 16-32) |

---

## 📊 Recommended Settings (16GB GPU)

```bash
python train.py --epochs 50 --batch_size 16
```

- Batch size 16: ~700 MB (safe)
- Batch size 32: ~1.2 GB (safe)
- Batch size 64: ~2.4 GB (if data fits)

---

## 📁 Files to Transfer

1. **Code:** All `.py` files
2. **Dataset:** `360dataset/` folder
3. **Scripts:** `train_uvpfl.sh`, `test_gpu.sh`
4. **Config:** `requirements.txt`

---

## 🎯 Checklist

- [ ] Modules loaded
- [ ] Environment created
- [ ] Dependencies installed
- [ ] GPU verified (`nvidia-smi` + TensorFlow)
- [ ] Code transferred
- [ ] Dataset transferred
- [ ] Job script edited (paths!)
- [ ] Test job submitted

---

**Full guide:** See `PARAMSHIVAY_SETUP.md`

