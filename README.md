# UVPFL - User Profile-Based Viewport Prediction Using Federated Learning

Complete implementation of the research paper: "User Profile-Based Viewport Prediction Using Federated Learning (UVPFL) in 360-degree Real-Time Video Streaming"

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Dataset Setup](#dataset-setup)
4. [Running the Implementation](#running-the-implementation)
5. [Step-by-Step Execution](#step-by-step-execution)
6. [Jupyter Notebook Guide](#jupyter-notebook-guide)
7. [VS Code Guide](#vs-code-guide)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.8+
- CUDA-capable GPU (8GB+ recommended) OR CPU
- ~3 GB free disk space
- Dataset: 360° Video Viewing Dataset (already downloaded in `360dataset/`)

---

## Installation

### 1. Install Dependencies

```bash
cd /home/arunabha/Shini/UVPFL
pip install -r requirements.txt
```

### 2. Verify Environment

```bash
python3 verify_environment.py
```

This will check:
- ✅ TensorFlow with GPU support
- ✅ All required packages
- ✅ Model components (ResNet50, GRU)

---

## Dataset Setup

The dataset should already be in `360dataset/` folder. If not:

1. Download from: https://aiins.cs.nthu.edu.tw/360-video-project/
2. Extract to `360dataset/` folder

**Dataset Structure:**
```
360dataset/
├── content/
│   ├── saliency/     # Saliency videos
│   └── motion/       # Motion videos
└── sensory/
    ├── orientation/  # Head movement data (Y, PI, R)
    ├── tile/         # Tile data
    └── raw/         # Raw sensor data
```

---

## Running the Implementation

### Option 1: Complete Pipeline (Recommended)

Run the main script that executes everything:

```bash
python3 main.py
```

This will:
1. ✅ Verify environment
2. ✅ Preprocess data (if needed)
3. ✅ Train the model
4. ✅ Evaluate results

### Option 2: Step-by-Step Execution

See [Step-by-Step Execution](#step-by-step-execution) below.

---

## Step-by-Step Execution

### STEP 0: Verify Environment

```bash
python3 verify_environment.py
```

**Expected Output:**
```
✅ TensorFlow: 2.20.0
✅ GPU Available: 1 device(s)
✅ All dependencies installed correctly!
```

---

### STEP 1: Data Preprocessing

**Purpose:** Organize data by user and video category (as per paper)

```bash
python3 data_preprocessing.py
```

**What it does:**
- Separates data for each user (50 users)
- Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
- Extracts orientation data (Y, PI, R)
- Creates user profiles for similarity matching
- Creates train/test split (80/20)

**Output:**
- `processed_data/` folder with organized data
- `processed_data/train_test_split.json` - Train/test user IDs
- `processed_data/user_profiles/` - User profiles by category

**Time:** ~30 seconds

---

### STEP 2: Test Data Loader

**Purpose:** Verify data loading works correctly

```python
# In Python or Jupyter
from data_loader import UVPFLDataLoaderFast

loader = UVPFLDataLoaderFast(
    dataset_path='360dataset',
    processed_path='processed_data',
    batch_size=8
)

# Get a sample batch
train_gen = loader.train_generator()
frames, targets = next(train_gen)

print(f"Frames shape: {frames.shape}")  # (8, 30, 120, 240, 3)
print(f"Targets shape: {targets.shape}")  # (8, 3)
```

---

### STEP 3: Test Model Architecture

**Purpose:** Verify model can be created and run forward pass

```python
from model import UVPFLModel
import numpy as np

# Create model
model = UVPFLModel(model_type='resnet50', freeze_backbone=True)

# Print summary
model.summary()

# Test forward pass
dummy_input = np.random.rand(2, 30, 120, 240, 3).astype(np.float32)
output = model.predict(dummy_input)
print(f"Output shape: {output.shape}")  # (2, 3)
```

---

### STEP 4: Test Viewport Prediction

**Purpose:** Verify similar user matching and viewport prediction

```bash
python3 viewport_prediction.py
```

**Expected Output:**
```
✅ Similar users found
✅ Viewport overlap calculation works
✅ Tile probability calculation works
```

---

### STEP 5: Test Tile Adaptation

**Purpose:** Verify tile quality assignment

```bash
python3 tile_adaptation.py
```

**Expected Output:**
```
✅ Quality assignment works
✅ Bandwidth savings: ~75%
```

---

### STEP 6: Train the Model

**Quick Training (for testing):**
```bash
python3 train.py --quick --quick_epochs 3 --batch_size 4
```

**Full Training (50 epochs as per paper):**
```bash
python3 train.py --epochs 50 --batch_size 8
```

**Training Options:**
```bash
# Use MobileNet (lighter, faster)
python3 train.py --model_type mobilenet --epochs 50

# Unfreeze backbone for fine-tuning
python3 train.py --unfreeze_backbone --epochs 50

# Custom learning rate
python3 train.py --learning_rate 0.0001 --epochs 50
```

**Output:**
- `checkpoints/` - Model checkpoints
- `logs/` - Training logs and TensorBoard files

**Note:** If GPU license error occurs, use CPU:
```bash
CUDA_VISIBLE_DEVICES="" python3 train.py --quick --quick_epochs 3
```

---

## Jupyter Notebook Guide

### Create Jupyter Notebook

1. **Install Jupyter:**
```bash
pip install jupyter ipykernel
```

2. **Create notebook:**
```bash
jupyter notebook
```

3. **Create new notebook:** `UVPFL_Complete.ipynb`

### Notebook Cells

#### Cell 1: Setup and Imports
```python
import sys
import os
sys.path.append('/home/arunabha/Shini/UVPFL')

import numpy as np
import tensorflow as tf
from pathlib import Path

# Enable GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print(f"GPU: {gpus[0].name}")
else:
    print("Using CPU")
```

#### Cell 2: Verify Environment
```python
%run verify_environment.py
```

#### Cell 3: Data Preprocessing
```python
from data_preprocessing import UVPFLDataPreprocessor

preprocessor = UVPFLDataPreprocessor(
    dataset_path='360dataset',
    output_path='processed_data'
)

# Run preprocessing
preprocessor.process_all_data()

# Create train/test split
preprocessor.create_train_test_split(test_ratio=0.2)
```

#### Cell 4: Test Data Loader
```python
from data_loader import UVPFLDataLoaderFast

loader = UVPFLDataLoaderFast(
    dataset_path='360dataset',
    processed_path='processed_data',
    batch_size=4
)

# Get sample
train_gen = loader.train_generator()
frames, targets = next(train_gen)
print(f"Frames: {frames.shape}, Targets: {targets.shape}")
```

#### Cell 5: Create Model
```python
from model import UVPFLModel

model = UVPFLModel(
    model_type='resnet50',
    freeze_backbone=True,
    learning_rate=0.001
)

model.summary()
```

#### Cell 6: Train Model
```python
# Get data generators
train_gen = loader.train_generator(shuffle=True)
val_gen = loader.test_generator()

# Train
history = model.model.fit(
    train_gen,
    steps_per_epoch=100,  # Adjust based on your needs
    epochs=5,  # Start with 5, then do 50
    validation_data=val_gen,
    validation_steps=50,
    verbose=1
)
```

#### Cell 7: Evaluate Model
```python
# Evaluate
test_gen = loader.test_generator()
results = model.model.evaluate(test_gen, steps=100, return_dict=True)

print("Evaluation Results:")
for metric, value in results.items():
    print(f"  {metric}: {value:.4f}")
```

#### Cell 8: Test Viewport Prediction
```python
from viewport_prediction import ViewportPredictor, UserProfile

# Create predictor
predictor = ViewportPredictor(
    model=model.model,
    processed_path='processed_data'
)

# Test prediction
test_profile = UserProfile(
    user_id=1, video_name='pacman', category='cg_fast_paced',
    mean_yaw=0.5, std_yaw=10.0, mean_pitch=2.0, std_pitch=5.0,
    mean_roll=0.0, std_roll=2.0, mean_speed=1.5, std_speed=0.8
)

# Predict viewport
viewport, was_merged = predictor.predict_with_similar_users(
    frames=frames[0],  # Single sequence
    current_orientation=targets[0],
    current_profile=test_profile,
    frame_idx=100
)

print(f"Predicted viewport: yaw={viewport.yaw:.2f}°, pitch={viewport.pitch:.2f}°")
print(f"Merged with similar user: {was_merged}")
```

#### Cell 9: Test Tile Adaptation
```python
from tile_adaptation import TileAdapter

adapter = TileAdapter()
assignments = adapter.assign_quality(viewport)
bandwidth = adapter.calculate_bandwidth(assignments)

print(f"VP tiles: {len(assignments['VP'])}")
print(f"VN tiles: {len(assignments['VN'])}")
print(f"VZ tiles: {len(assignments['VZ'])}")
print(f"Bandwidth savings: {bandwidth['bandwidth_savings_percent']:.1f}%")
```

---

## VS Code Guide

### 1. Open Project in VS Code

```bash
code /home/arunabha/Shini/UVPFL
```

### 2. Create Python Script: `run_complete.py`

See the `run_complete.py` file (created below) for a complete execution script.

### 3. Run in VS Code

- **Method 1:** Use the run button (▶️) in VS Code
- **Method 2:** Press `F5` to debug
- **Method 3:** Right-click → "Run Python File in Terminal"
- **Method 4:** Use integrated terminal: `python3 run_complete.py`

### 4. Debugging

- Set breakpoints by clicking left of line numbers
- Press `F5` to start debugging
- Use debug console to inspect variables

---

## Complete Execution Script

Create `run_complete.py` (see below) for one-command execution.

---

## Troubleshooting

### GPU License Error

**Error:** `device doesn't have valid Grid license`

**Solution:** Use CPU instead:
```bash
CUDA_VISIBLE_DEVICES="" python3 train.py --quick
```

Or in Python:
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Out of Memory

**Error:** `OOM (Out of Memory)`

**Solutions:**
1. Reduce batch size: `--batch_size 4` or `--batch_size 2`
2. Use MobileNet: `--model_type mobilenet`
3. Use CPU: `CUDA_VISIBLE_DEVICES="" python3 train.py`

### Missing Data

**Error:** `File not found: processed_data/...`

**Solution:** Run preprocessing first:
```bash
python3 data_preprocessing.py
```

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

---

## File Structure

```
UVPFL/
├── 360dataset/              # Original dataset (1.7 GB)
├── processed_data/           # Preprocessed data (186 MB)
├── checkpoints/             # Model checkpoints (created during training)
├── logs/                    # Training logs (created during training)
│
├── data_preprocessing.py    # Step 1: Data preprocessing
├── data_loader.py           # Step 2: Data loading
├── model.py                 # Step 3: Model architecture
├── viewport_prediction.py   # Step 4: Viewport prediction
├── tile_adaptation.py       # Step 5: Tile adaptation
├── train.py                 # Step 6: Training pipeline
├── run_complete.py          # Complete execution script
├── verify_environment.py     # Environment verification
│
├── requirements.txt         # Dependencies
├── README.md                # This file
└── STORAGE_ANALYSIS.md      # Storage usage analysis
```

---

## Quick Start (One Command)

```bash
python3 run_complete.py
```

This runs everything automatically!

---

## Expected Results (from Paper)

- **Accuracy:** 96% for 1-second horizon
- **First 7 seconds:** 86% accuracy
- **Bandwidth savings:** ~75% with tile adaptation
- **Training time:** ~2-3 hours for 50 epochs (on GPU)

---

## Next Steps

After training:
1. Evaluate model: `python3 evaluate.py` (to be created)
2. Compare with SOTA: `python3 compare_sota.py` (to be created)
3. Generate plots: `python3 visualize_results.py` (to be created)

---

## Support

For issues:
1. Check `verify_environment.py` output
2. Check GPU/CPU availability
3. Verify dataset is in `360dataset/` folder
4. Check disk space: `df -h`

