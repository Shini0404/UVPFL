# UVPFL Data Flow - Simple Explanation

## 📖 What Does This Project Do?

**Imagine you're watching a 360° video on YouTube (like a virtual reality video).**
- The video is all around you (360 degrees)
- But you can only see a small part at a time (your "viewport")
- **The goal:** Predict where you'll look next so we can stream that part in high quality

**Real-world analogy:**
- Like Netflix pre-loading the next scene before you watch it
- But instead of "next scene," we predict "where will your eyes move next" in 360° videos
- This saves bandwidth and makes videos smoother

---

## 🔄 Complete Data Flow (Step by Step)

### **STEP 1: Raw Input Data** 📥

**What we start with:**

```
360dataset/
├── content/
│   └── saliency/          # Videos with "attraction maps" (what's interesting)
│       ├── coaster_saliency.mp4
│       ├── pacman_saliency.mp4
│       └── ... (10 videos total)
│
└── sensory/
    └── orientation/       # Head movement data (50 users × 10 videos)
        ├── coaster_user01_orientation.csv  (Yaw, Pitch, Roll angles)
        ├── coaster_user02_orientation.csv
        └── ... (500 files total)
```

**What each file contains:**

1. **Saliency Videos** (`saliency/`):
   - Regular videos but with heat maps showing "interesting" areas
   - Like highlighting the most eye-catching parts in each frame
   - **Example:** In a roller coaster video, the track and scenery are highlighted

2. **Orientation Files** (`orientation/`):
   - CSV files with head movement data
   - Each row = one frame of video
   - Columns: `Yaw`, `Pitch`, `Roll` (how the head is oriented)
   - **Example:**
     ```
     Frame, Yaw, Pitch, Roll
     0,     10.5, 2.3,  0.1
     1,     12.1, 2.5,  0.2
     2,     13.8, 2.7,  0.1
     ```
   - These are the "answers" - where people actually looked

---

### **STEP 2: Data Preprocessing** 🔧
**File:** `data_preprocessing.py`

**What happens:**
Like organizing a messy room into labeled boxes

1. **Read all files:**
   - Loads 10 videos
   - Loads 500 orientation files (50 users × 10 videos)

2. **Organize by user:**
   - Groups data by user (User 1, User 2, ..., User 50)
   - Each user watched all 10 videos

3. **Organize by video category:**
   - **CG Fast-paced:** Pacman, Game, Ride
   - **NI Fast-paced:** Coaster, Coaster2  
   - **NI Slow-paced:** Diving, Drive, Landscape, Panel, Sport

4. **Create "sequences":**
   - Takes 30 frames at a time (1 second of video at 30fps)
   - Pairs each sequence with the "answer" (where they looked after those 30 frames)
   - **Example:**
     ```
     Sequence: Frames 0-29 → Answer: Where they looked at frame 59 (1 second later)
     Sequence: Frames 15-44 → Answer: Where they looked at frame 74
     ```

5. **Split into train/test:**
   - 80% users for training (40 users)
   - 20% users for testing (10 users)

**Output:** `processed_data/` folder with organized data

```
processed_data/
├── cg_fast_paced/
│   └── pacman/
│       └── user01/
│           ├── orientation.npy    # All head movements for this user+video
│           └── profile.json       # Summary of user's behavior
├── train_test_split.json          # Which users are train/test
└── config.json                    # Dataset configuration
```

---

### **STEP 3: Frame Preprocessing (Optional but Recommended)** 🎬
**File:** `preprocess_frames.py`

**What happens:**
Instead of loading frames from video files every time (slow!), we extract all frames and save them as numpy arrays (fast!)

**Input:**
- Video files: `coaster_saliency.mp4` (has ~1800 frames)

**Process:**
1. Open video file
2. Extract each frame
3. Resize to 240×120 pixels
4. Convert to RGB format
5. Save as numpy array

**Output:**
- `coaster_frames.npy` - Contains all ~1800 frames as one array
- Loading this is 100-1000× faster than loading from video file!

**Why this matters:**
- Without preprocessing: 1 training epoch = 61 hours ❌
- With preprocessing: 1 training epoch = 5-15 minutes ✅

---

### **STEP 4: Data Loading for Training** 📦
**File:** `data_loader.py`

**What happens:**
Like a waiter bringing food to your table - serves data in batches to the model

**For each training step:**

1. **Pick a random sample:**
   - Example: User 5, Video "coaster", starting at frame 100

2. **Load 30 frames:**
   - Frames 100-129 from the video
   - Shape: `(30, 120, 240, 3)` = 30 frames × 120 height × 240 width × 3 colors
   - If preprocessed: Loads from `.npy` file (fast!)
   - If not: Extracts from video file (slow!)

3. **Load the target answer:**
   - Where did the user look at frame 159? (100 + 30 + 29)
   - Answer: `[Yaw=15.2, Pitch=3.1, Roll=0.5]`

4. **Create a batch:**
   - Repeat steps 1-3 for 16 samples (batch size = 16)
   - Batch shape: `(16, 30, 120, 240, 3)` - 16 sequences of 30 frames
   - Target shape: `(16, 3)` - 16 answers

5. **Normalize data:**
   - Convert pixel values from 0-255 to 0-1 (easier for model)
   - Normalize angles (if needed)

**Output:** Ready-to-use batches for training

---

### **STEP 5: Model Architecture** 🧠
**File:** `model.py`

**What the model does:**
Like a smart assistant that watches the last 1 second of video and predicts where you'll look next

**Model structure:**

```
INPUT: 30 frames of video (1 second)
  ↓
[ResNet50] - Looks at each frame and extracts "features" (what's happening)
  ↓
[TimeDistributed] - Applies ResNet50 to all 30 frames
  ↓
30 feature vectors (one per frame)
  ↓
[GRU] - Understands the sequence/movement pattern
  ↓
1 combined feature vector (understands the whole 1 second)
  ↓
[Dense Layers] - Makes the final prediction
  ↓
OUTPUT: [Yaw, Pitch, Roll] - Where the user will look next
```

**Analogy:**
- **ResNet50:** "What's interesting in each frame?" (image understanding)
- **GRU:** "How is the user moving their head?" (sequence understanding)
- **Dense:** "Based on both, where will they look next?" (prediction)

**Numbers:**
- Input shape: `(batch, 30, 120, 240, 3)`
- Output shape: `(batch, 3)` = (Yaw, Pitch, Roll)
- Total parameters: 24.4 million
- Trainable: 845K (ResNet50 is frozen, only GRU + Dense layers learn)

---

### **STEP 6: Training Process** 🏋️
**File:** `train.py`

**What happens:**
The model learns by making mistakes and correcting itself

**Training loop (for 50 epochs):**

1. **Forward Pass:**
   - Model sees: 30 frames of video
   - Model predicts: `[Yaw=12.0, Pitch=2.5, Roll=0.3]`
   - Actual answer: `[Yaw=15.2, Pitch=3.1, Roll=0.5]`
   - **Error:** The difference between prediction and actual

2. **Calculate Loss:**
   - Loss = Mean Squared Error (MSE)
   - Measures how wrong the prediction was
   - Example: `Loss = 1467.65` (high = bad, low = good)

3. **Backward Pass (Learning):**
   - Model says: "I was wrong by this much"
   - Adjusts internal parameters (weights) to reduce error
   - Like adjusting a dial to get closer to the right answer

4. **Repeat:**
   - Do this for all training samples
   - After 1 epoch, repeat 49 more times
   - Loss should decrease: `1467 → 800 → 400 → 200 → ...`

**Metrics tracked:**
- **Loss (MSE):** How wrong the predictions are (lower is better)
- **MAE:** Mean Absolute Error (easier to interpret)
- **Validation Loss:** Performance on test set (should be similar to training)

**Output:**
- Trained model saved in `checkpoints/`
- Training history (loss over time)
- Model learns patterns like:
  - "When coaster goes up, users look up (positive pitch)"
  - "In Pacman, users follow the character (yaw changes)"

---

### **STEP 7: Viewport Prediction (For New Users)** 👤→🎯
**File:** `viewport_prediction.py`

**Problem:** What if a new user starts watching? We have no history!

**Solution:** Find similar users and use their behavior

**Process:**

1. **Calculate User Profile:**
   - For a new user watching first 5 seconds
   - Calculate: average head movement, speed, patterns
   - Example: `{mean_yaw=10.5, mean_pitch=2.3, speed=1.5}`

2. **Find Similar Users:**
   - Compare new user's profile with trained users
   - Use cosine similarity (measures how similar two vectors are)
   - Find top 3 most similar users
   - Example: "User 5, User 12, and User 23 are similar"

3. **Merge Predictions:**
   - Model predicts: `VP = [Yaw=12.0, Pitch=2.5, Roll=0.3]` (viewport)
   - Similar user's actual viewport: `VS = [Yaw=13.5, Pitch=2.8, Roll=0.2]`
   - Calculate overlap (how much do they overlap?)
   - If overlap > 80%: Merge them for better prediction
   - Final: `V_merged = weighted_average(VP, VS)`

4. **Tile Probability Calculation:**
   - Divide 360° video into tiles (like a grid)
   - Calculate probability each tile will be visible
   - Use Equation 1 from paper (Zou et al.)
   - Example: Tile in center = 95% probability, tile on edge = 5%

**Output:**
- Predicted viewport: `(Yaw, Pitch, Roll)`
- Tile visibility probabilities: Which tiles are most likely visible
- Quality assignment: High/Medium/Low quality for each tile

---

### **STEP 8: Tile Adaptation** 🎨
**File:** `tile_adaptation.py`

**What happens:**
Assign video quality based on predicted viewport

**Process:**

1. **Group Tiles by Probability:**
   - **Group 1 (Viewport):** Tiles definitely visible → High quality
   - **Group 2 (>98%):** Very likely visible → High quality
   - **Group 3 (95-98%):** Likely visible → Medium quality
   - **Group 4 (90-95%):** Maybe visible → Medium quality
   - **Others (<90%):** Unlikely visible → Low quality

2. **Assign Quality:**
   - High quality: 1080p (clear, detailed)
   - Medium quality: 720p (decent)
   - Low quality: 360p (saves bandwidth)

3. **Stream to User:**
   - Only tiles in viewport at high quality
   - Saves 80%+ bandwidth!
   - User sees high quality where they're looking

**Output:**
- Quality assignment map
- Bandwidth calculation
- Adaptive streaming configuration

---

### **STEP 9: Evaluation** 📊
**File:** `evaluate.py`

**What happens:**
Measure how good the model is

**Metrics:**

1. **Accuracy:**
   - % of predictions within acceptable range
   - Paper target: 96% for 1-second horizon
   - Example: "96 out of 100 predictions were correct"

2. **Precision:**
   - Of all tiles predicted as "visible," how many were actually visible?
   - Paper: 92.41% for 1-second horizon

3. **Recall:**
   - Of all actually visible tiles, how many did we predict?
   - Paper: 90.15% for 1-second horizon

4. **F1-Score:**
   - Combined measure of precision and recall

5. **Comparison with SOTA:**
   - Compare with other methods (Mosaic, Flare, Sparkle)
   - UVPFL should beat them: +4.1% vs Mosaic, +64.9% vs Flare, +1.12% vs Sparkle

**Output:**
- Evaluation metrics
- Comparison plots
- Model performance report

---

## 📊 Complete Data Flow Diagram

```
RAW DATA (360dataset/)
    ↓
[Data Preprocessing] → organized by user + category
    ↓
PROCESSED DATA (processed_data/)
    ↓
[Frame Preprocessing] → extract frames as .npy files (optional)
    ↓
PREPROCESSED FRAMES (processed_data/frames/)
    ↓
[Data Loader] → creates batches of (frames, targets)
    ↓
TRAINING BATCHES: (16, 30, 120, 240, 3) + (16, 3)
    ↓
[MODEL TRAINING]
    ↓
    [ResNet50] → extract features from frames
    ↓
    [GRU] → understand sequence
    ↓
    [Dense] → predict (Yaw, Pitch, Roll)
    ↓
PREDICTIONS: (16, 3)
    ↓
[Calculate Loss] → compare with actual
    ↓
[Update Weights] → learn from mistakes
    ↓
TRAINED MODEL (checkpoints/)
    ↓
[Viewport Prediction] → for new users (similar user matching)
    ↓
[Tile Adaptation] → assign quality levels
    ↓
FINAL OUTPUT: Adaptive streaming configuration
    ↓
[Evaluation] → measure accuracy, precision, recall
```

---

## 🔑 Key Concepts Explained Simply

### **Yaw, Pitch, Roll (Head Orientation)**
- **Yaw:** Left/Right head rotation (like shaking head "no")
- **Pitch:** Up/Down head rotation (like nodding "yes")
- **Roll:** Tilt head left/right (like tilting head in confusion)

Together, these 3 numbers describe exactly where you're looking in 360° space.

### **Saliency Maps**
- Heat maps showing "interesting" areas in video
- Red = very interesting, Blue = less interesting
- Helps model focus on important areas

### **Federated Learning**
- Each user's data stays on their device (privacy)
- Only model updates are shared
- No raw data leaves the user's device

### **Viewport**
- The visible area you see in a 360° video
- Like the "window" through which you view the world
- Usually ~90-120° horizontally, 90° vertically

### **Tiles**
- The 360° video is divided into a grid (tiles)
- Each tile is a small rectangular region
- We predict which tiles will be visible and stream them at high quality

---

## 📝 Summary: What Goes In, What Comes Out

### **INPUT:**
1. **10 Saliency Videos** (what's interesting in each frame)
2. **500 Orientation Files** (where 50 users looked while watching 10 videos)
3. **Video metadata** (frame count, FPS, etc.)

### **PROCESSING:**
1. **Organize** data by user and video category
2. **Extract** frames and create sequences
3. **Train** model to predict head movement
4. **Match** similar users for new user predictions

### **OUTPUT:**
1. **Trained Model** that predicts viewport
2. **User Profiles** for similarity matching
3. **Tile Quality Map** (which tiles at what quality)
4. **Evaluation Metrics** (accuracy: 96%, precision: 92.41%, recall: 90.15%)

### **END RESULT:**
An adaptive streaming system that:
- Predicts where users will look in 360° videos
- Streams high quality only where needed
- Saves 80%+ bandwidth
- Improves user experience

---

## 🎯 Real-World Example

**Scenario:** User watches "Roller Coaster" 360° video

1. **User starts watching:**
   - System loads first 30 frames
   - Model predicts: "User will look slightly up and right" (Pitch=+5°, Yaw=+10°)

2. **If new user:**
   - System finds similar users (users who also looked up during coaster climbs)
   - Merges predictions for better accuracy

3. **Adaptive streaming:**
   - High quality: Center viewport + surrounding areas
   - Medium quality: Areas user might look next
   - Low quality: Everything else

4. **Result:**
   - Smooth, high-quality viewing experience
   - Uses 80% less bandwidth than streaming full 360° at high quality
   - User doesn't notice - they see high quality where they're looking

---

That's the complete data flow! Simple, right? 😊

