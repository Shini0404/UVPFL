# UVPFL Quick Start Guide

## 🚀 Fastest Way to Run Everything

### Option 1: One Command (Recommended)

```bash
cd /home/arunabha/Shini/UVPFL
python3 run_complete.py
```

This will:
- ✅ Verify environment
- ✅ Preprocess data (if needed)
- ✅ Test all components
- ✅ Train the model

### Option 2: With CPU (if GPU license issues)

```bash
python3 run_complete.py --use_cpu --quick
```

---

## 📝 Step-by-Step Manual Execution

### In VS Code or Terminal:

#### 1. Verify Environment
```bash
python3 verify_environment.py
```

#### 2. Preprocess Data (if not done)
```bash
python3 data_preprocessing.py
```

#### 3. Test Components
```bash
# Test data loader
python3 -c "from data_loader import UVPFLDataLoaderFast; loader = UVPFLDataLoaderFast(); print('✅ Data loader works')"

# Test viewport prediction
python3 viewport_prediction.py

# Test tile adaptation
python3 tile_adaptation.py
```

#### 4. Train Model

**Quick test (3 epochs):**
```bash
python3 train.py --quick --quick_epochs 3 --batch_size 4
```

**Full training (50 epochs):**
```bash
python3 train.py --epochs 50 --batch_size 8
```

**With CPU (if GPU issues):**
```bash
CUDA_VISIBLE_DEVICES="" python3 train.py --quick --quick_epochs 3
```

---

## 📓 Jupyter Notebook

### 1. Start Jupyter
```bash
cd /home/arunabha/Shini/UVPFL
jupyter notebook
```

### 2. Open Notebook
- Open `UVPFL_Complete.ipynb`
- Run cells sequentially (Shift+Enter)

### 3. Or Create New Notebook
- Copy code from `UVPFL_Complete.ipynb`
- Run each cell

---

## 🔧 Common Commands

### Check GPU
```bash
nvidia-smi
```

### Use CPU Instead
```bash
CUDA_VISIBLE_DEVICES="" python3 <script>.py
```

### Check Storage
```bash
df -h .
du -sh *
```

### Clean Cache (free space)
```bash
pip cache purge
```

---

## 📊 What Each File Does

| File | Purpose | When to Run |
|------|---------|-------------|
| `verify_environment.py` | Check setup | First time |
| `data_preprocessing.py` | Organize data | Once (or if data changes) |
| `data_loader.py` | Load data for training | Automatically used |
| `model.py` | Model architecture | Automatically used |
| `viewport_prediction.py` | Similar user matching | Test or use in pipeline |
| `tile_adaptation.py` | Quality assignment | Test or use in pipeline |
| `train.py` | Train model | After preprocessing |
| `run_complete.py` | Run everything | **Main entry point** |

---

## ⚠️ Troubleshooting

### GPU License Error
**Error:** `device doesn't have valid Grid license`

**Fix:**
```bash
CUDA_VISIBLE_DEVICES="" python3 run_complete.py --use_cpu
```

### Out of Memory
**Fix:**
- Reduce batch size: `--batch_size 4` or `2`
- Use MobileNet: `--model_type mobilenet`

### Missing Data
**Fix:**
```bash
python3 data_preprocessing.py
```

---

## ✅ Success Indicators

After running `run_complete.py`, you should see:
- ✅ Environment verification passed
- ✅ Data preprocessing complete
- ✅ Data loader works
- ✅ Model created successfully
- ✅ Training started/completed

---

## 📁 Output Files

After running, you'll have:
- `processed_data/` - Preprocessed data
- `checkpoints/` - Trained models
- `logs/` - Training logs

---

## 🎯 Next Steps After Training

1. **Evaluate model:**
   ```python
   from model import UVPFLModel
   model = UVPFLModel.load('checkpoints/uvpfl_resnet50_best.keras')
   # Evaluate...
   ```

2. **Use for prediction:**
   ```python
   from viewport_prediction import ViewportPredictor
   predictor = ViewportPredictor(model=model.model)
   # Predict viewport...
   ```

---

## 📞 Quick Reference

**Run everything:**
```bash
python3 run_complete.py
```

**Quick test:**
```bash
python3 run_complete.py --quick
```

**With CPU:**
```bash
python3 run_complete.py --use_cpu
```

**Skip preprocessing:**
```bash
python3 run_complete.py --skip_preprocessing
```

