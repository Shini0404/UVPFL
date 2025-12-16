"""
UVPFL Environment Verification Script
Run this script to verify all dependencies are correctly installed.
"""

import sys

def verify_environment():
    print("=" * 60)
    print("UVPFL Environment Verification")
    print("=" * 60)
    
    errors = []
    
    # TensorFlow
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow: {tf.__version__}")
        
        # GPU Check
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU Available: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"   - {gpu.name}")
        else:
            print("⚠️  No GPU detected - will use CPU (slower training)")
    except ImportError as e:
        errors.append(f"TensorFlow: {e}")
        print(f"❌ TensorFlow: Not installed")
    
    # Keras
    try:
        from tensorflow import keras
        print(f"✅ Keras: {keras.__version__}")
    except ImportError as e:
        errors.append(f"Keras: {e}")
        print(f"❌ Keras: Not installed")
    
    # NumPy
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        errors.append(f"NumPy: {e}")
        print(f"❌ NumPy: Not installed")
    
    # Pandas
    try:
        import pandas as pd
        print(f"✅ Pandas: {pd.__version__}")
    except ImportError as e:
        errors.append(f"Pandas: {e}")
        print(f"❌ Pandas: Not installed")
    
    # OpenCV
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        errors.append(f"OpenCV: {e}")
        print(f"❌ OpenCV: Not installed")
    
    # Scikit-learn
    try:
        import sklearn
        print(f"✅ Scikit-learn: {sklearn.__version__}")
    except ImportError as e:
        errors.append(f"Scikit-learn: {e}")
        print(f"❌ Scikit-learn: Not installed")
    
    # Matplotlib
    try:
        import matplotlib
        print(f"✅ Matplotlib: {matplotlib.__version__}")
    except ImportError as e:
        errors.append(f"Matplotlib: {e}")
        print(f"❌ Matplotlib: Not installed")
    
    # TQDM
    try:
        import tqdm
        print(f"✅ TQDM: {tqdm.__version__}")
    except ImportError as e:
        errors.append(f"TQDM: {e}")
        print(f"❌ TQDM: Not installed")
    
    # PIL
    try:
        from PIL import Image
        import PIL
        print(f"✅ Pillow: {PIL.__version__}")
    except ImportError as e:
        errors.append(f"Pillow: {e}")
        print(f"❌ Pillow: Not installed")
    
    # Check required model components
    print("\n" + "-" * 40)
    print("Model Components Check:")
    print("-" * 40)
    
    try:
        from tensorflow.keras.applications import ResNet50
        print("✅ ResNet50: Available")
    except Exception as e:
        errors.append(f"ResNet50: {e}")
        print(f"❌ ResNet50: {e}")
    
    try:
        from tensorflow.keras.layers import GRU, TimeDistributed, Dense, Flatten
        print("✅ GRU + TimeDistributed: Available")
    except Exception as e:
        errors.append(f"GRU: {e}")
        print(f"❌ GRU: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ Environment has {len(errors)} error(s):")
        for err in errors:
            print(f"   - {err}")
        print("\nRun: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed correctly!")
        print("✅ Ready to run UVPFL implementation!")
        return True
    print("=" * 60)


def check_gpu_memory():
    """Check available GPU memory."""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            # Enable memory growth to avoid OOM
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("\n✅ GPU memory growth enabled (prevents OOM)")
    except Exception as e:
        print(f"⚠️  Could not configure GPU memory: {e}")


def test_model_creation():
    """Test that we can create the UVPFL model architecture."""
    print("\n" + "-" * 40)
    print("Testing Model Architecture:")
    print("-" * 40)
    
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import ResNet50
        from tensorflow.keras.layers import GRU, TimeDistributed, Dense, Flatten, Input
        from tensorflow.keras.models import Model
        
        # Model parameters from paper
        SEQUENCE_LENGTH = 30
        FRAME_HEIGHT = 120
        FRAME_WIDTH = 240
        CHANNELS = 3
        
        # Test with smaller batch for verification
        print(f"Input shape: ({SEQUENCE_LENGTH}, {FRAME_HEIGHT}, {FRAME_WIDTH}, {CHANNELS})")
        
        # Create a simple test
        input_shape = (SEQUENCE_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS)
        inputs = Input(shape=input_shape)
        
        # ResNet50 base (without top)
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg',
                              input_shape=(FRAME_HEIGHT, FRAME_WIDTH, CHANNELS))
        
        # TimeDistributed wrapper
        x = TimeDistributed(base_model)(inputs)
        
        # GRU layer
        x = GRU(128, return_sequences=False)(x)
        
        # Output: Y, PI, R (Yaw, Pitch, Roll)
        outputs = Dense(3, name='viewport_prediction')(x)
        
        model = Model(inputs=inputs, outputs=outputs)
        
        print(f"✅ Model created successfully!")
        print(f"   Total parameters: {model.count_params():,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False


if __name__ == "__main__":
    success = verify_environment()
    if success:
        check_gpu_memory()
        test_model_creation()
    sys.exit(0 if success else 1)

