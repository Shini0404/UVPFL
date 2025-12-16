# UVPFL Execution Guide - Complete Instructions

## 🎯 Quick Answer: How to Run Everything

### **EASIEST WAY (One Command):**

```bash
cd /home/arunabha/Shini/UVPFL
python3 run_complete.py
```

**That's it!** This runs the entire pipeline automatically.

---

## 📋 Detailed Step-by-Step Instructions

### **Method 1: VS Code**

1. **Open VS Code:**
   ```bash
   code /home/arunabha/Shini/UVPFL
   ```

2. **Open the main script:**
   - File: `run_complete.py`

3. **Run it:**
   - **Option A:** Click the ▶️ (Run) button at top right
   - **Option B:** Press `F5` (Debug)
   - **Option C:** Right-click file → "Run Python File in Terminal"
   - **Option D:** Open terminal (Ctrl+`) → Type: `python3 run_complete.py`

4. **If GPU license error:**
   - Edit `run_complete.py`
   - Add `--use_cpu` to arguments, OR
   - Run in terminal: `python3 run_complete.py --use_cpu`

---

### **Method 2: Terminal/Command Line**

1. **Navigate to project:**
   ```bash
   cd /home/arunabha/Shini/UVPFL
   ```

2. **Run complete pipeline:**
   ```bash
   python3 run_complete.py
   ```

3. **Options:**
   ```bash
   # Quick test (faster)
   python3 run_complete.py --quick
   
   # Use CPU (if GPU issues)
   python3 run_complete.py --use_cpu
   
   # Skip preprocessing (if already done)
   python3 run_complete.py --skip_preprocessing
   ```

---

### **Method 3: Jupyter Notebook**

1. **Start Jupyter:**
   ```bash
   cd /home/arunabha/Shini/UVPFL
   jupyter notebook
   ```

2. **Open notebook:**
   - Click on `UVPFL_Complete.ipynb`

3. **Run all cells:**
   - Menu: **Cell → Run All**
   - Or run each cell with **Shift+Enter**

4. **If GPU issues:**
   - In first cell, add:
   ```python
   import os
   os.environ['CUDA_VISIBLE_DEVICES'] = ''
   ```

---

## 🔧 Running Individual Steps

If you want to run each step separately:

### Step 1: Verify Environment
```bash
python3 verify_environment.py
```

### Step 2: Preprocess Data
```bash
python3 data_preprocessing.py
```
**Time:** ~30 seconds  
**Output:** `processed_data/` folder

### Step 3: Test Data Loader
```python
python3 -c "from data_loader import UVPFLDataLoaderFast; loader = UVPFLDataLoaderFast(); print('✅ Works')"
```

### Step 4: Test Model
```python
python3 -c "from model import UVPFLModel; m = UVPFLModel(); print('✅ Works')"
```

### Step 5: Test Viewport Prediction
```bash
python3 viewport_prediction.py
```

### Step 6: Test Tile Adaptation
```bash
python3 tile_adaptation.py
```

### Step 7: Train Model

**Quick test (3 epochs):**
```bash
python3 train.py --quick --quick_epochs 3 --batch_size 4
```

**Full training (50 epochs):**
```bash
python3 train.py --epochs 50 --batch_size 8
```

**With CPU:**
```bash
CUDA_VISIBLE_DEVICES="" python3 train.py --quick
```

---

## ⚙️ Command Options Reference

### `run_complete.py` Options

```bash
# Basic
python3 run_complete.py

# Quick mode (faster, for testing)
python3 run_complete.py --quick

# Use CPU (if GPU license issues)
python3 run_complete.py --use_cpu

# Skip preprocessing
python3 run_complete.py --skip_preprocessing

# Skip training (only test components)
python3 run_complete.py --skip_training

# Custom epochs
python3 run_complete.py --epochs 10 --batch_size 4

# Combine options
python3 run_complete.py --use_cpu --quick --skip_preprocessing
```

### `train.py` Options

```bash
# Quick training
python3 train.py --quick --quick_epochs 3

# Full training
python3 train.py --epochs 50 --batch_size 8

# Use MobileNet (lighter)
python3 train.py --model_type mobilenet --epochs 50

# Custom learning rate
python3 train.py --learning_rate 0.0001 --epochs 50

# With CPU
CUDA_VISIBLE_DEVICES="" python3 train.py --quick
```

---

## 🐛 Troubleshooting

### Problem 1: GPU License Error
**Error:** `device doesn't have valid Grid license` or `cudaSetDevice() failed`

**Solution:**
```bash
# Method 1: Use --use_cpu flag
python3 run_complete.py --use_cpu

# Method 2: Set environment variable
CUDA_VISIBLE_DEVICES="" python3 run_complete.py

# Method 3: In Python code
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Problem 2: Out of Memory
**Error:** `OOM (Out of Memory)`

**Solution:**
```bash
# Reduce batch size
python3 train.py --batch_size 4

# Or use lighter model
python3 train.py --model_type mobilenet --batch_size 4
```

### Problem 3: Missing Processed Data
**Error:** `File not found: processed_data/...`

**Solution:**
```bash
python3 data_preprocessing.py
```

### Problem 4: Import Errors
**Error:** `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem 5: Training Too Slow
**Solution:**
- Use `--quick` mode for testing
- Use smaller batch size
- Use MobileNet instead of ResNet50
- Use CPU if GPU license issues

---

## 📊 Expected Execution Flow

When you run `python3 run_complete.py`, you'll see:

```
============================================================
UVPFL Complete Pipeline Execution
============================================================

STEP 0: Environment Verification
✅ All dependencies installed correctly!

STEP 1: Data Preprocessing
✅ Processed data already exists!

STEP 2: Testing Data Loader
✅ Data loader works!
   Train samples: 46400
   Test samples: 11600

STEP 3: Testing Model Architecture
✅ Model works!
   Total parameters: 24,432,515

STEP 4: Testing Viewport Prediction
✅ Viewport prediction works!

STEP 5: Testing Tile Adaptation
✅ Tile adaptation works!

STEP 6: Training Model
Epoch 1/50
...
✅ Training complete!

============================================================
✅ ALL STEPS COMPLETED SUCCESSFULLY!
============================================================
```

---

## 📁 What Gets Created

After running, you'll have:

```
UVPFL/
├── processed_data/          # Preprocessed data (186 MB)
│   ├── cg_fast_paced/       # CG fast-paced videos
│   ├── ni_fast_paced/       # NI fast-paced videos
│   ├── ni_slow_paced/       # NI slow-paced videos
│   ├── user_profiles/       # User profiles for FL
│   └── train_test_split.json
│
├── checkpoints/             # Model checkpoints (after training)
│   ├── uvpfl_resnet50_best.keras
│   └── uvpfl_resnet50_latest.keras
│
└── logs/                    # Training logs (after training)
    ├── training.csv
    └── tensorboard_logs/
```

---

## ✅ Verification Checklist

Before running, check:

- [ ] Dataset exists: `ls 360dataset/`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Environment verified: `python3 verify_environment.py`
- [ ] Enough disk space: `df -h .` (need ~3 GB)

---

## 🎓 For Different Use Cases

### **Just Testing (Quick)**
```bash
python3 run_complete.py --quick --skip_training
```

### **Full Training**
```bash
python3 run_complete.py --epochs 50
```

### **CPU Only (No GPU)**
```bash
python3 run_complete.py --use_cpu --quick
```

### **Already Preprocessed**
```bash
python3 run_complete.py --skip_preprocessing
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Run everything | `python3 run_complete.py` |
| Quick test | `python3 run_complete.py --quick` |
| Use CPU | `python3 run_complete.py --use_cpu` |
| Train only | `python3 train.py --quick` |
| Verify setup | `python3 verify_environment.py` |
| Preprocess data | `python3 data_preprocessing.py` |

---

## 🎯 Summary

**To run everything:**
```bash
cd /home/arunabha/Shini/UVPFL
python3 run_complete.py
```

**If GPU issues:**
```bash
python3 run_complete.py --use_cpu
```

**That's it!** 🎉

For more details, see:
- `README.md` - Full documentation
- `QUICK_START.md` - Quick reference
- `HOW_TO_RUN.md` - Detailed guide

