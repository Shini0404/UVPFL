"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

import os
import cv2
import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Generator
from tqdm import tqdm


# ============================================================================
# CONFIGURATION (from paper)
# ============================================================================
SEQUENCE_LENGTH = 30      # frames per sequence
FRAME_HEIGHT = 120        # height
FRAME_WIDTH = 240         # width
CHANNELS = 3              # RGB
PREDICTION_HORIZON = 30   # predict 1 second ahead (30 frames at 30fps)


class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand.
    Caches video capture objects for efficiency.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder
            target_size: (width, height) for resizing frames
        """
        self.saliency_path = Path(saliency_path)
        self.target_size = target_size
        self._video_captures = {}  # Cache for video capture objects
        self._video_frame_counts = {}
    
    def get_video_path(self, video_name: str) -> Path:
        """Get path to saliency video."""
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """Get total frame count for a video."""
        if video_name not in self._video_frame_counts:
            video_path = self.get_video_path(video_name)
            cap = cv2.VideoCapture(str(video_path))
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video.
        
        Args:
            video_name: Name of the video
            frame_idx: Frame index (0-based)
            
        Returns:
            Frame as numpy array (height, width, channels) normalized to [0, 1]
        """
        video_path = self.get_video_path(video_name)
        
        # Create new capture for each extraction (thread-safe)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            # Return black frame if extraction fails
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame
        frame = cv2.resize(frame, self.target_size)
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        frame = frame.astype(np.float32) / 255.0
        
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of frames from the video.
        
        Args:
            video_name: Name of the video
            start_frame: Starting frame index
            sequence_length: Number of frames to extract
            
        Returns:
            Sequence as numpy array (sequence_length, height, width, channels)
        """
        video_path = self.get_video_path(video_name)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        for _ in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                # Pad with black frames if video ends
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize and convert
            frame = cv2.resize(frame, self.target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
        
        cap.release()
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """Close all cached video captures."""
        for cap in self._video_captures.values():
            cap.release()
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()

