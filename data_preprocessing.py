"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import json
import gc
from typing import Dict, List, Tuple, Optional

# Video category mapping from Paper Figure 7
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],
    'ni_fast_paced': ['coaster', 'coaster2'],
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']
}

VIDEO_TO_CATEGORY = {}
for category, videos in VIDEO_CATEGORIES.items():
    for video in videos:
        VIDEO_TO_CATEGORY[video] = category

VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster', 'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck', 'drive': 'Driving With',
    'game': 'Hog Rider', 'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man', 'panel': 'Perils Penal',
    'ride': 'Chariot Race', 'sport': 'SFR Sport'
}

ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())
NUM_USERS = 50
SEQUENCE_LENGTH = 30
FRAME_HEIGHT = 120
FRAME_WIDTH = 240
CHANNELS = 3


class UVPFLDataPreprocessor:
    def __init__(self, dataset_path: str, output_path: str):
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path)
        self.saliency_path = self.dataset_path / 'content' / 'saliency'
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'
        self.tile_path = self.dataset_path / 'sensory' / 'tile'
        self._create_output_directories()
        self.stats = {'total_frames': 0, 'total_sequences': 0, 'users_processed': 0, 'videos_processed': 0}
    
    def _create_output_directories(self):
        self.output_path.mkdir(parents=True, exist_ok=True)
        for category in VIDEO_CATEGORIES.keys():
            cat_path = self.output_path / category
            cat_path.mkdir(exist_ok=True)
            for video in VIDEO_CATEGORIES[category]:
                (cat_path / video).mkdir(exist_ok=True)
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'
        if not video_path.exists():
            return None
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        metadata = {
            'video_name': video_name, 'category': VIDEO_TO_CATEGORY[video_name],
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'saliency_video_path': str(video_path)
        }
        cap.release()
        return metadata
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        if not file_path.exists():
            return None
        df = pd.read_csv(file_path, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        if not file_path.exists():
            return None
        tiles_data = []
        with open(file_path, 'r') as f:
            f.readline()
            for line in f:
                parts = line.strip().split(',')
                frame_no = int(parts[0].strip())
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        return tiles_data
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        yaw, pitch, roll = df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values
        d_yaw, d_pitch, d_roll = np.diff(yaw, prepend=yaw[0]), np.diff(pitch, prepend=pitch[0]), np.diff(roll, prepend=roll[0])
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        df = self.load_orientation_data(video_name, user_id)
        if df is None:
            return None
        tile_data = self.load_tile_data(video_name, user_id)
        speed = self.calculate_head_movement_speed(df)
        category = VIDEO_TO_CATEGORY[video_name]
        num_frames = len(df)
        
        profile = {
            'user_id': user_id, 'video_name': video_name, 'category': category,
            'num_frames': num_frames, 'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            'mean_yaw': float(df['cal. yaw'].mean()), 'std_yaw': float(df['cal. yaw'].std()),
            'mean_pitch': float(df['cal. pitch'].mean()), 'std_pitch': float(df['cal. pitch'].std()),
            'mean_roll': float(df['cal. roll'].mean()), 'std_roll': float(df['cal. roll'].std()),
            'mean_speed': float(speed.mean()), 'std_speed': float(speed.std())
        }
        
        orientation_array = np.column_stack([df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values])
        return {'orientation_array': orientation_array, 'tile_data': tile_data, 'speed': speed, 'profile': profile}
    
    def process_all_data(self):
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        video_metadata = {}
        
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            metadata = self.get_video_metadata(video_name)
            if metadata is None:
                continue
            
            video_metadata[video_name] = metadata
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats['videos_processed'] += 1
            self.stats['total_frames'] += metadata['frame_count']
            category = VIDEO_TO_CATEGORY[video_name]
            
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                result = self.process_user_video(video_name, user_id)
                if result is None:
                    continue
                
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                np.save(user_dir / 'speed.npy', result['speed'])
                if result['tile_data']:
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)
                
                all_profiles[category].append(result['profile'])
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            self.stats['users_processed'] += NUM_USERS
            gc.collect()
        
        # Save profiles
        for cat, profiles in all_profiles.items():
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)
        
        # Save metadata
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        config = {
            'video_categories': VIDEO_CATEGORIES, 'video_to_category': VIDEO_TO_CATEGORY,
            'video_name_mapping': VIDEO_NAME_MAPPING, 'all_videos': ALL_VIDEOS,
            'num_users': NUM_USERS, 'sequence_length': SEQUENCE_LENGTH,
            'frame_height': FRAME_HEIGHT, 'frame_width': FRAME_WIDTH
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        return all_profiles
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()
