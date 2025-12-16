# How to Run UVPFL - Complete Guide

## 🎯 Three Ways to Run

### Method 1: One Command (Easiest) ⭐

```bash
cd /home/arunabha/Shini/UVPFL
python3 run_complete.py
```

**That's it!** This runs everything automatically.

---

### Method 2: VS Code

1. **Open VS Code:**
   ```bash
   code /home/arunabha/Shini/UVPFL
   ```

2. **Open `run_complete.py`**

3. **Run it:**
   - Click the ▶️ button, OR
   - Press `F5` (debug), OR
   - Right-click → "Run Python File in Terminal"

4. **Or run in terminal:**
   - Open terminal in VS Code (Ctrl+`)
   - Type: `python3 run_complete.py`

---

### Method 3: Jupyter Notebook

1. **Start Jupyter:**
   ```bash
   cd /home/arunabha/Shini/UVPFL
   jupyter notebook
   ```

2. **Open `UVPFL_Complete.ipynb`**

3. **Run all cells:**
   - Menu: Cell → Run All
   - Or run each cell with Shift+Enter

---

## 📋 Step-by-Step Manual Execution

If you want to run each step separately:

### Step 1: Verify Setup
```bash
python3 verify_environment.py
```

### Step 2: Preprocess Data (if not done)
```bash
python3 data_preprocessing.py
```

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

**Quick test:**
```bash
python3 train.py --quick --quick_epochs 3
```

**Full training:**
```bash
python3 train.py --epochs 50 --batch_size 8
```

---

## 🔧 Command Options

### Complete Pipeline Options

```bash
# Quick mode (faster, for testing)
python3 run_complete.py --quick

# Use CPU (if GPU license issues)
python3 run_complete.py --use_cpu

# Skip preprocessing (if already done)
python3 run_complete.py --skip_preprocessing

# Skip training (only test components)
python3 run_complete.py --skip_training

# Custom epochs
python3 run_complete.py --epochs 10 --batch_size 4
```

### Training Options

```bash
# Quick training (3 epochs, small batch)
python3 train.py --quick --quick_epochs 3 --batch_size 4

# Full training (50 epochs as per paper)
python3 train.py --epochs 50 --batch_size 8

# Use MobileNet (lighter, faster)
python3 train.py --model_type mobilenet --epochs 50

# Use CPU
CUDA_VISIBLE_DEVICES="" python3 train.py --quick
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: GPU License Error
**Error:** `device doesn't have valid Grid license`

**Solution:**
```bash
# Use CPU instead
CUDA_VISIBLE_DEVICES="" python3 run_complete.py --use_cpu
```

Or in Python:
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Issue 2: Out of Memory
**Error:** `OOM (Out of Memory)`

**Solution:**
```bash
# Reduce batch size
python3 train.py --batch_size 4

# Or use lighter model
python3 train.py --model_type mobilenet --batch_size 4
```

### Issue 3: Missing Processed Data
**Error:** `File not found: processed_data/...`

**Solution:**
```bash
python3 data_preprocessing.py
```

### Issue 4: Import Errors
**Error:** `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📊 Expected Output

### Successful Run Output:

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

## 📁 File Structure

```
UVPFL/
├── run_complete.py          ⭐ MAIN SCRIPT - Run this!
├── README.md                 Full documentation
├── QUICK_START.md            Quick reference
├── HOW_TO_RUN.md            This file
│
├── verify_environment.py     Environment check
├── data_preprocessing.py     Step 1: Preprocess data
├── data_loader.py           Step 2: Load data
├── model.py                 Step 3: Model architecture
├── viewport_prediction.py   Step 4: Viewport prediction
├── tile_adaptation.py       Step 5: Tile adaptation
├── train.py                 Step 6: Training
│
├── UVPFL_Complete.ipynb     Jupyter notebook version
│
├── 360dataset/              Original dataset
├── processed_data/          Preprocessed data
├── checkpoints/             Model checkpoints (after training)
└── logs/                    Training logs (after training)
```

---

## 🎓 Learning Path

### Beginner:
1. Run: `python3 run_complete.py --quick`
2. Check output files in `checkpoints/` and `logs/`

### Intermediate:
1. Run each step manually
2. Modify parameters in scripts
3. Experiment with different models

### Advanced:
1. Modify model architecture
2. Implement custom loss functions
3. Add evaluation metrics

---

## 💡 Pro Tips

1. **First time?** Run with `--quick` to test everything
2. **GPU issues?** Always use `--use_cpu` flag
3. **Low memory?** Use `--batch_size 4` or `2`
4. **Want faster?** Use `--model_type mobilenet`
5. **Already processed?** Use `--skip_preprocessing`

---

## ✅ Checklist Before Running

- [ ] Dataset in `360dataset/` folder
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Environment verified: `python3 verify_environment.py`
- [ ] Enough disk space (~3 GB)
- [ ] GPU available OR ready to use CPU

---

## 🚀 Quick Commands Reference

```bash
# Run everything
python3 run_complete.py

# Quick test
python3 run_complete.py --quick

# With CPU
python3 run_complete.py --use_cpu

# Train only
python3 train.py --quick

# Full training
python3 train.py --epochs 50
```

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Check `QUICK_START.md` for quick reference
3. Run `python3 verify_environment.py` to diagnose issues
4. Check error messages - they usually tell you what's wrong

---

**That's it! You're ready to run UVPFL! 🎉**

