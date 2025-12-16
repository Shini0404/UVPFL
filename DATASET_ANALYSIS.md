# Dataset Analysis - UVPFL Implementation

## Dataset Structure

### Videos (10 total)
1. **coaster** - Roller Coaster (NI fast-paced)
2. **coaster2** - Mega Coaster (NI fast-paced)  
3. **diving** - Shark Shipwreck (NI slow-paced)
4. **drive** - Driving With (NI slow-paced)
5. **game** - Hog Rider (CG fast-paced)
6. **landscape** - Kangaroo Island (NI slow-paced)
7. **pacman** - Pac Man (CG fast-paced)
8. **panel** - Perils Penal (NI slow-paced)
9. **ride** - Chariot Race (CG fast-paced)
10. **sport** - SFR Sport (NI slow-paced)

### Dataset Organization

```
360dataset/
├── content/
│   ├── saliency/          # Saliency maps per frame (MP4 videos)
│   │   ├── coaster_saliency.mp4
│   │   ├── coaster2_saliency.mp4
│   │   └── ... (10 videos)
│   └── motion/            # Optical flow (MP4 videos)
│       ├── coaster_motion.mp4
│       └── ... (10 videos)
│
└── sensory/
    ├── orientation/       # Head movement data (CSV) - **PRIMARY DATA**
    │   ├── {video}_user{01-50}_orientation.csv
    │   └── ... (500 files: 10 videos × 50 users)
    ├── raw/               # Raw sensor data with timestamps
    │   └── {video}_user{01-50}_raw.csv
    └── tile/              # Tile numbers overlapped with FoV
        └── {video}_user{01-50}_tile.csv
```

## Data Format Analysis

### 1. Orientation Data (PRIMARY - Used in Algorithm)
**File**: `{video}_user{01-50}_orientation.csv`

**Columns**:
- `no. frames`: Frame number (00001, 00002, ...)
- `raw x, raw y, raw z`: Raw position coordinates
- `raw yaw, raw pitch, raw roll`: Raw head orientation angles
- **`cal. yaw, cal. pitch, cal. roll`**: **CALIBRATED ANGLES (Y, PI, R) - USED IN ALGORITHM**

**Key Data for UVPFL**:
- **Y (Yaw)**: `cal. yaw` column
- **PI (Pitch)**: `cal. pitch` column  
- **R (Roll)**: `cal. roll` column
- Frame-aligned data (already synchronized with video frames)

**Sample**: ~1800 frames per video (60 seconds @ 30 fps)

### 2. Tile Data
**File**: `{video}_user{01-50}_tile.csv`

**Columns**:
- `no. frames`: Frame number
- `tile numbers`: Comma-separated list of tile IDs overlapped with FoV
- **Tile size**: 192×192 pixels (as per readme)

**Usage**: 
- Validates viewport predictions
- Understands tile structure for tiling implementation

### 3. Saliency Data
**File**: `content/saliency/{video}_saliency.mp4`

**Content**: Video with saliency heat maps per frame
- Based on Cornia's saliency prediction method
- Indicates attraction level of each pixel/frame
- **Required as input for Algorithm 1**

### 4. Raw Data (Optional)
**File**: `sensory/raw/{video}_user{01-50}_raw.csv`

**Columns**: timestamp, rawTX, rawTY, rawTZ, rawYaw, rawPitch, rawRoll
- Raw sensor data with timestamps
- Not directly used (orientation data is frame-aligned version)

## What We Need for UVPFL Implementation

### ✅ Available in Dataset:
1. **360-degree videos** - Need to extract original videos (may need to download separately or extract from saliency videos)
2. **Saliency feature data** - ✅ Available in `content/saliency/`
3. **Head movement data (Y, PI, R)** - ✅ Available in `sensory/orientation/` (cal. yaw, cal. pitch, cal. roll)
4. **Frame-aligned data** - ✅ Already aligned in orientation files
5. **Tile information** - ✅ Available in `sensory/tile/` (192×192 tile size)

### 📋 Data Mapping to Paper:

**Video Categories** (based on paper's Fig. 7):
- **CG Fast-paced**: pacman, game, ride
- **NI Fast-paced**: coaster, coaster2
- **NI Slow-paced**: diving, drive, landscape, panel, sport

**Users**: 50 users (user01 to user50)

**Data per user-video pair**:
- Orientation CSV: ~1800 frames of head movement data
- Tile CSV: ~1800 frames of tile overlap data
- Saliency video: Full video with saliency maps

## Implementation Requirements

### Phase 1: Server-Side Processing
- ✅ Saliency maps: Available as MP4 videos (need to extract frames)
- ✅ Video frames: Need to extract from saliency videos or get original videos
- ⚠️ Video tiling: Need to implement l×k grid tiling (paper doesn't specify exact grid size)

### Phase 2: Client-Side Viewport Prediction
- ✅ Head movement data: `cal. yaw`, `cal. pitch`, `cal. roll` from orientation CSV
- ✅ Frame alignment: Already done in dataset
- ⚠️ Head movement speed: Need to calculate from consecutive frames
- ⚠️ Similar user matching: Need to implement based on viewing patterns per category

### Phase 3: Tile Adaptation
- ✅ Tile structure: 192×192 pixels (from readme)
- ⚠️ Viewport coordinates: Need to convert Y, PI, R to viewport coordinates
- ⚠️ Tile quality assignment: Need to implement hierarchical quality assignment

## Next Steps

1. **Extract video frames** from saliency videos or obtain original 360° videos
2. **Parse orientation CSVs** to extract Y, PI, R angles per frame
3. **Organize data by user and video category** for federated learning
4. **Implement video tiling** (l×k grid - need to determine optimal size)
5. **Extract saliency maps** from saliency videos frame-by-frame
6. **Calculate head movement speed** from orientation data
7. **Implement similar user matching** algorithm

