"""
UVPFL Complete Execution Script

This script runs the entire UVPFL pipeline from start to finish:
1. Environment verification
2. Data preprocessing (if needed)
3. Model training
4. Evaluation

Usage:
    python3 run_complete.py [--skip_preprocessing] [--quick] [--epochs N]
"""

import os
import sys
import argparse
from pathlib import Path
import json

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Check for CPU flag BEFORE importing TensorFlow
if '--use_cpu' in sys.argv or os.environ.get('FORCE_CPU', '').lower() == 'true':
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    print("⚠️  CPU mode enabled (GPU disabled)")

import tensorflow as tf

# Enable GPU memory growth (if GPU available)
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU available: {gpus[0].name}")
    else:
        print("⚠️  No GPU available, using CPU")
except Exception as e:
    print(f"⚠️  GPU setup failed, using CPU: {e}")
    os.environ['CUDA_VISIBLE_DEVICES'] = ''


def step_0_verify_environment():
    """Step 0: Verify environment."""
    print("\n" + "=" * 60)
    print("STEP 0: Environment Verification")
    print("=" * 60)
    
    try:
        from verify_environment import verify_environment, check_gpu_memory, test_model_creation
        
        if not verify_environment():
            print("❌ Environment verification failed!")
            return False
        
        check_gpu_memory()
        test_model_creation()
        
        print("✅ Environment verification passed!")
        return True
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False


def step_1_preprocess_data(force: bool = False):
    """Step 1: Data preprocessing."""
    print("\n" + "=" * 60)
    print("STEP 1: Data Preprocessing")
    print("=" * 60)
    
    processed_path = Path('processed_data')
    
    # Check if already processed
    if processed_path.exists() and not force:
        config_file = processed_path / 'config.json'
        if config_file.exists():
            print("✅ Processed data already exists!")
            print("   Use --force to reprocess")
            return True
    
    try:
        from data_preprocessing import UVPFLDataPreprocessor
        
        preprocessor = UVPFLDataPreprocessor(
            dataset_path='360dataset',
            output_path='processed_data'
        )
        
        preprocessor.process_all_data()
        preprocessor.create_train_test_split(test_ratio=0.2)
        
        print("✅ Data preprocessing complete!")
        return True
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_2_test_data_loader():
    """Step 2: Test data loader."""
    print("\n" + "=" * 60)
    print("STEP 2: Testing Data Loader")
    print("=" * 60)
    
    try:
        from data_loader import UVPFLDataLoaderFast
        
        loader = UVPFLDataLoaderFast(
            dataset_path='360dataset',
            processed_path='processed_data',
            batch_size=4
        )
        
        # Get a sample batch
        train_gen = loader.train_generator()
        frames, targets = next(train_gen)
        
        print(f"✅ Data loader works!")
        print(f"   Frames shape: {frames.shape}")
        print(f"   Targets shape: {targets.shape}")
        print(f"   Train samples: {len(loader.train_samples)}")
        print(f"   Test samples: {len(loader.test_samples)}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing data loader: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_3_test_model(use_cpu: bool = False):
    """Step 3: Test model architecture."""
    print("\n" + "=" * 60)
    print("STEP 3: Testing Model Architecture")
    print("=" * 60)
    
    # Force CPU if requested
    if use_cpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        print("⚠️  Using CPU (GPU disabled)")
        # Clear any existing TensorFlow session
        tf.keras.backend.clear_session()
    
    try:
        from model import UVPFLModel
        import numpy as np
        
        # Try to create model
        try:
            model = UVPFLModel(
                model_type='resnet50',
                freeze_backbone=True
            )
        except Exception as gpu_error:
            # If GPU error, force CPU and retry
            if 'cuda' in str(gpu_error).lower() or 'gpu' in str(gpu_error).lower() or 'device' in str(gpu_error).lower():
                print("⚠️  GPU error detected, switching to CPU...")
                os.environ['CUDA_VISIBLE_DEVICES'] = ''
                tf.keras.backend.clear_session()
                # Re-import after clearing
                import importlib
                import model
                importlib.reload(model)
                model = model.UVPFLModel(
                    model_type='resnet50',
                    freeze_backbone=True
                )
            else:
                raise
        
        # Test forward pass
        dummy_input = np.random.rand(2, 30, 120, 240, 3).astype(np.float32)
        output = model.predict(dummy_input)
        
        print(f"✅ Model works!")
        print(f"   Input shape: {dummy_input.shape}")
        print(f"   Output shape: {output.shape}")
        print(f"   Total parameters: {model.model.count_params():,}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        print("\n💡 Try with CPU: python3 run_complete.py --use_cpu")
        import traceback
        traceback.print_exc()
        return False


def step_4_test_viewport_prediction():
    """Step 4: Test viewport prediction."""
    print("\n" + "=" * 60)
    print("STEP 4: Testing Viewport Prediction")
    print("=" * 60)
    
    try:
        from viewport_prediction import SimilarUserMatcher, Viewport, ViewportPredictor
        from viewport_prediction import UserProfile
        
        # Test similar user matcher
        matcher = SimilarUserMatcher('processed_data')
        print(f"✅ Similar user matcher loaded")
        print(f"   Categories: {list(matcher.profiles.keys())}")
        
        # Test viewport operations
        vp1 = Viewport(yaw=10.0, pitch=5.0, roll=0.0)
        vp2 = Viewport(yaw=15.0, pitch=8.0, roll=0.0)
        
        predictor = ViewportPredictor(model=None, processed_path='processed_data')
        overlap = predictor.calculate_viewport_overlap(vp1, vp2)
        
        print(f"✅ Viewport operations work!")
        print(f"   Viewport overlap: {overlap:.2%}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing viewport prediction: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_5_test_tile_adaptation():
    """Step 5: Test tile adaptation."""
    print("\n" + "=" * 60)
    print("STEP 5: Testing Tile Adaptation")
    print("=" * 60)
    
    try:
        from tile_adaptation import TileAdapter
        from viewport_prediction import Viewport
        
        adapter = TileAdapter()
        viewport = Viewport(yaw=0.0, pitch=0.0, roll=0.0)
        
        assignments = adapter.assign_quality(viewport)
        bandwidth = adapter.calculate_bandwidth(assignments)
        
        print(f"✅ Tile adaptation works!")
        print(f"   VP tiles: {len(assignments['VP'])}")
        print(f"   VN tiles: {len(assignments['VN'])}")
        print(f"   VZ tiles: {len(assignments['VZ'])}")
        print(f"   Bandwidth savings: {bandwidth['bandwidth_savings_percent']:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Error testing tile adaptation: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_6_train_model(quick: bool = False, epochs: int = 50, batch_size: int = 8):
    """Step 6: Train the model."""
    print("\n" + "=" * 60)
    print("STEP 6: Training Model")
    print("=" * 60)
    
    if quick:
        print("🚀 Quick training mode (for testing)")
        epochs = 3
        batch_size = 4
    
    try:
        from train import quick_train, create_training_config, train_model
        from data_loader import UVPFLDataLoaderFast
        from model import UVPFLModel
        
        if quick:
            # Quick training
            model, history = quick_train(epochs=epochs, batch_size=batch_size)
        else:
            # Full training
            config = create_training_config(argparse.Namespace(
                model_type='resnet50',
                batch_size=batch_size,
                epochs=epochs,
                learning_rate=0.001,
                gru_units=128,
                dropout_rate=0.3,
                unfreeze_backbone=False,
                dataset_path='360dataset',
                processed_path='processed_data',
                checkpoint_dir='checkpoints',
                log_dir='logs'
            ))
            model, history = train_model(config)
        
        print("✅ Training complete!")
        return True
    except Exception as e:
        print(f"❌ Error during training: {e}")
        print("\n💡 Tip: If GPU license error, use CPU:")
        print("   CUDA_VISIBLE_DEVICES=\"\" python3 run_complete.py --quick")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='UVPFL Complete Pipeline')
    
    parser.add_argument('--skip_preprocessing', action='store_true',
                        help='Skip data preprocessing if already done')
    parser.add_argument('--force_preprocessing', action='store_true',
                        help='Force data preprocessing even if already done')
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode (skip some tests, quick training)')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs (default: 50)')
    parser.add_argument('--batch_size', type=int, default=8,
                        help='Batch size (default: 8)')
    parser.add_argument('--skip_training', action='store_true',
                        help='Skip training (only test components)')
    parser.add_argument('--use_cpu', action='store_true',
                        help='Force CPU usage (if GPU license issues)')
    
    args = parser.parse_args()
    
    # Force CPU if requested
    if args.use_cpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        print("⚠️  Using CPU (GPU disabled)")
    
    print("=" * 60)
    print("UVPFL Complete Pipeline Execution")
    print("=" * 60)
    print(f"Quick mode: {args.quick}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print("=" * 60)
    
    # Step 0: Verify environment
    if not step_0_verify_environment():
        print("\n❌ Environment verification failed. Please fix issues first.")
        return
    
    # Step 1: Preprocess data
    if not args.skip_preprocessing:
        if not step_1_preprocess_data(force=args.force_preprocessing):
            print("\n❌ Data preprocessing failed.")
            return
    else:
        print("\n⏭️  Skipping data preprocessing")
    
    # Step 2: Test data loader
    if not step_2_test_data_loader():
        print("\n❌ Data loader test failed.")
        return
    
    # Step 3: Test model
    if not step_3_test_model(use_cpu=args.use_cpu):
        print("\n❌ Model test failed.")
        if not args.use_cpu:
            print("\n💡 Try with CPU: python3 run_complete.py --use_cpu")
        return
    
    # Step 4: Test viewport prediction
    if not step_4_test_viewport_prediction():
        print("\n❌ Viewport prediction test failed.")
        return
    
    # Step 5: Test tile adaptation
    if not step_5_test_tile_adaptation():
        print("\n❌ Tile adaptation test failed.")
        return
    
    # Step 6: Train model
    if not args.skip_training:
        if not step_6_train_model(quick=args.quick, epochs=args.epochs, batch_size=args.batch_size):
            print("\n❌ Training failed.")
            print("\n💡 Try with CPU if GPU license error:")
            print("   python3 run_complete.py --use_cpu --quick")
            return
    else:
        print("\n⏭️  Skipping training")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check checkpoints/ for trained models")
    print("2. Check logs/ for training history")
    print("3. Run evaluation: python3 evaluate.py (to be created)")
    print("=" * 60)


if __name__ == '__main__':
    main()

