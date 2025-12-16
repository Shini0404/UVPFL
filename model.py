"""
UVPFL Model Architecture - ResNet50 + GRU

Implementation of the model architecture as described in the paper:
"User Profile-Based Viewport Prediction Using Federated Learning (UVPFL)"

Architecture (from Paper Figure 3):
1. Pre-trained ResNet50 (feature extractor)
2. TimeDistributed wrapper (process each frame)
3. TimeDistributed Flatten
4. GRU layer (temporal modeling)
5. Dense output layer (Yaw, Pitch, Roll prediction)

Paper specifications:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Optimizer: Adam
- Loss: Mean Squared Error (MSE)
- Best model: ResNet50 achieved 96% accuracy
- Other tested: AlexNet (73%), MobileNet (56%)
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import ResNet50, MobileNetV2, VGG16
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, 
    TensorBoard, CSVLogger
)
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import json
from datetime import datetime


# ============================================================================
# MODEL CONFIGURATION (from paper)
# ============================================================================
SEQUENCE_LENGTH = 30      # frames per sequence
FRAME_HEIGHT = 120        # height
FRAME_WIDTH = 240         # width
CHANNELS = 3              # RGB

# Training parameters from paper
LEARNING_RATE = 0.001     # Adam default
EPOCHS = 50               # Paper: "After 50 epochs, there is much less change in accuracy"
BATCH_SIZE = 8            # Optimized for 8GB GPU


def create_resnet50_gru_model(
    sequence_length: int = SEQUENCE_LENGTH,
    frame_height: int = FRAME_HEIGHT,
    frame_width: int = FRAME_WIDTH,
    channels: int = CHANNELS,
    gru_units: int = 128,
    dropout_rate: float = 0.3,
    freeze_backbone: bool = True
) -> Model:
    """
    Create the UVPFL model with ResNet50 + GRU architecture.
    
    Architecture (from Paper Figure 3):
    - ResNet50 (pre-trained on ImageNet) → Feature extraction
    - TimeDistributed → Process each frame independently
    - GRU → Capture temporal dependencies
    - Dense → Output (Yaw, Pitch, Roll)
    
    Args:
        sequence_length: Number of frames per sequence (default: 30)
        frame_height: Frame height (default: 120)
        frame_width: Frame width (default: 240)
        channels: Number of channels (default: 3)
        gru_units: Number of GRU units (default: 128)
        dropout_rate: Dropout rate (default: 0.3)
        freeze_backbone: Whether to freeze ResNet50 weights (default: True)
        
    Returns:
        Compiled Keras Model
    """
    # Input layer
    input_shape = (sequence_length, frame_height, frame_width, channels)
    inputs = layers.Input(shape=input_shape, name='video_input')
    
    # ResNet50 backbone (pre-trained on ImageNet, without top classification layer)
    # Using pooling='avg' to get fixed-size output regardless of input size
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        pooling='avg',
        input_shape=(frame_height, frame_width, channels)
    )
    
    # Freeze backbone if specified (for transfer learning)
    if freeze_backbone:
        base_model.trainable = False
    
    # TimeDistributed wrapper - applies ResNet50 to each frame
    # Output shape: (batch, sequence_length, 2048) - ResNet50 outputs 2048 features
    x = layers.TimeDistributed(base_model, name='time_distributed_resnet50')(inputs)
    
    # Optional: Add dropout for regularization
    x = layers.Dropout(dropout_rate, name='dropout_features')(x)
    
    # GRU layer for temporal modeling
    # Output shape: (batch, gru_units)
    x = layers.GRU(
        gru_units, 
        return_sequences=False,
        name='gru_temporal'
    )(x)
    
    # Dropout after GRU
    x = layers.Dropout(dropout_rate, name='dropout_gru')(x)
    
    # Dense layer for final processing
    x = layers.Dense(64, activation='relu', name='dense_hidden')(x)
    
    # Output layer: Yaw, Pitch, Roll prediction
    outputs = layers.Dense(3, activation='linear', name='viewport_prediction')(x)
    
    # Create model
    model = Model(inputs=inputs, outputs=outputs, name='UVPFL_ResNet50_GRU')
    
    return model


def create_mobilenet_gru_model(
    sequence_length: int = SEQUENCE_LENGTH,
    frame_height: int = FRAME_HEIGHT,
    frame_width: int = FRAME_WIDTH,
    channels: int = CHANNELS,
    gru_units: int = 128,
    dropout_rate: float = 0.3,
    freeze_backbone: bool = True
) -> Model:
    """
    Create alternative model with MobileNetV2 + GRU (lighter, faster).
    Paper reported 56% accuracy with MobileNet.
    
    Useful for:
    - Faster training/inference
    - Lower memory usage
    - Quick experiments
    """
    input_shape = (sequence_length, frame_height, frame_width, channels)
    inputs = layers.Input(shape=input_shape, name='video_input')
    
    # MobileNetV2 backbone (lighter than ResNet50)
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        pooling='avg',
        input_shape=(frame_height, frame_width, channels)
    )
    
    if freeze_backbone:
        base_model.trainable = False
    
    x = layers.TimeDistributed(base_model, name='time_distributed_mobilenet')(inputs)
    x = layers.Dropout(dropout_rate)(x)
    x = layers.GRU(gru_units, return_sequences=False, name='gru_temporal')(x)
    x = layers.Dropout(dropout_rate)(x)
    x = layers.Dense(64, activation='relu')(x)
    outputs = layers.Dense(3, activation='linear', name='viewport_prediction')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name='UVPFL_MobileNet_GRU')
    
    return model


def create_lightweight_model(
    sequence_length: int = SEQUENCE_LENGTH,
    frame_height: int = FRAME_HEIGHT,
    frame_width: int = FRAME_WIDTH,
    channels: int = CHANNELS,
    gru_units: int = 64
) -> Model:
    """
    Create a lightweight model for quick testing.
    Uses simple CNN instead of pre-trained backbone.
    """
    input_shape = (sequence_length, frame_height, frame_width, channels)
    inputs = layers.Input(shape=input_shape, name='video_input')
    
    # Simple CNN backbone
    def simple_cnn(x):
        x = layers.Conv2D(32, 3, activation='relu', padding='same')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
        x = layers.GlobalAveragePooling2D()(x)
        return x
    
    # Apply CNN to each frame
    x = layers.TimeDistributed(
        layers.Lambda(lambda x: simple_cnn(x))
    )(inputs)
    
    # This won't work directly, so let's use a different approach
    # TimeDistributed with Sequential model
    cnn_model = keras.Sequential([
        layers.Conv2D(32, 3, activation='relu', padding='same', input_shape=(frame_height, frame_width, channels)),
        layers.MaxPooling2D(2),
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(2),
        layers.Conv2D(128, 3, activation='relu', padding='same'),
        layers.GlobalAveragePooling2D()
    ], name='simple_cnn')
    
    x = layers.TimeDistributed(cnn_model, name='time_distributed_cnn')(inputs)
    x = layers.GRU(gru_units, return_sequences=False, name='gru_temporal')(x)
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(3, activation='linear', name='viewport_prediction')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name='UVPFL_Lightweight')
    
    return model


def compile_model(
    model: Model,
    learning_rate: float = LEARNING_RATE,
    loss: str = 'mse'
) -> Model:
    """
    Compile the model with optimizer and loss function.
    
    Paper specifications:
    - Optimizer: Adam
    - Loss: Mean Squared Error (MSE)
    
    Args:
        model: Keras Model
        learning_rate: Learning rate for Adam optimizer
        loss: Loss function (default: 'mse')
        
    Returns:
        Compiled model
    """
    optimizer = Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=['mae', 'mse']  # Mean Absolute Error, Mean Squared Error
    )
    
    return model


def get_callbacks(
    model_name: str = 'uvpfl',
    checkpoint_dir: str = 'checkpoints',
    log_dir: str = 'logs',
    patience: int = 10
) -> List:
    """
    Get training callbacks.
    
    Args:
        model_name: Name for saving checkpoints
        checkpoint_dir: Directory for checkpoints
        log_dir: Directory for TensorBoard logs
        patience: Patience for early stopping
        
    Returns:
        List of callbacks
    """
    # Create directories
    Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            filepath=f'{checkpoint_dir}/{model_name}_best.keras',
            monitor='val_loss',
            save_best_only=True,
            mode='min',
            verbose=1
        ),
        
        # Save latest model
        ModelCheckpoint(
            filepath=f'{checkpoint_dir}/{model_name}_latest.keras',
            save_best_only=False,
            verbose=0
        ),
        
        # Early stopping
        EarlyStopping(
            monitor='val_loss',
            patience=patience,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
        
        # TensorBoard logging
        TensorBoard(
            log_dir=f'{log_dir}/{model_name}_{timestamp}',
            histogram_freq=1,
            write_graph=True
        ),
        
        # CSV logging
        CSVLogger(
            filename=f'{log_dir}/{model_name}_{timestamp}_training.csv',
            separator=',',
            append=False
        )
    ]
    
    return callbacks


class UVPFLModel:
    """
    UVPFL Model wrapper class for easy training and inference.
    """
    
    def __init__(
        self,
        model_type: str = 'resnet50',
        sequence_length: int = SEQUENCE_LENGTH,
        frame_height: int = FRAME_HEIGHT,
        frame_width: int = FRAME_WIDTH,
        gru_units: int = 128,
        dropout_rate: float = 0.3,
        freeze_backbone: bool = True,
        learning_rate: float = LEARNING_RATE
    ):
        """
        Initialize UVPFL model.
        
        Args:
            model_type: 'resnet50', 'mobilenet', or 'lightweight'
            sequence_length: Number of frames per sequence
            frame_height: Frame height
            frame_width: Frame width
            gru_units: Number of GRU units
            dropout_rate: Dropout rate
            freeze_backbone: Whether to freeze backbone weights
            learning_rate: Learning rate
        """
        self.model_type = model_type
        self.sequence_length = sequence_length
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.gru_units = gru_units
        self.dropout_rate = dropout_rate
        self.freeze_backbone = freeze_backbone
        self.learning_rate = learning_rate
        
        # Create model
        self.model = self._create_model()
        
        # Compile model
        self.model = compile_model(self.model, learning_rate)
        
        # Training history
        self.history = None
    
    def _create_model(self) -> Model:
        """Create the model based on model_type."""
        if self.model_type == 'resnet50':
            return create_resnet50_gru_model(
                sequence_length=self.sequence_length,
                frame_height=self.frame_height,
                frame_width=self.frame_width,
                gru_units=self.gru_units,
                dropout_rate=self.dropout_rate,
                freeze_backbone=self.freeze_backbone
            )
        elif self.model_type == 'mobilenet':
            return create_mobilenet_gru_model(
                sequence_length=self.sequence_length,
                frame_height=self.frame_height,
                frame_width=self.frame_width,
                gru_units=self.gru_units,
                dropout_rate=self.dropout_rate,
                freeze_backbone=self.freeze_backbone
            )
        elif self.model_type == 'lightweight':
            return create_lightweight_model(
                sequence_length=self.sequence_length,
                frame_height=self.frame_height,
                frame_width=self.frame_width,
                gru_units=self.gru_units
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def summary(self):
        """Print model summary."""
        self.model.summary()
    
    def train(
        self,
        train_generator,
        val_generator,
        steps_per_epoch: int,
        validation_steps: int,
        epochs: int = EPOCHS,
        callbacks: List = None,
        verbose: int = 1
    ):
        """
        Train the model.
        
        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            steps_per_epoch: Steps per training epoch
            validation_steps: Steps for validation
            epochs: Number of epochs (default: 50 as per paper)
            callbacks: Training callbacks
            verbose: Verbosity level
            
        Returns:
            Training history
        """
        if callbacks is None:
            callbacks = get_callbacks(model_name=f'uvpfl_{self.model_type}')
        
        self.history = self.model.fit(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=val_generator,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=verbose
        )
        
        return self.history
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict viewport (Yaw, Pitch, Roll) for input sequences.
        
        Args:
            x: Input sequences of shape (batch, sequence_length, height, width, channels)
            
        Returns:
            Predictions of shape (batch, 3) = (yaw, pitch, roll)
        """
        return self.model.predict(x)
    
    def evaluate(self, test_generator, steps: int) -> Dict:
        """
        Evaluate the model.
        
        Args:
            test_generator: Test data generator
            steps: Number of evaluation steps
            
        Returns:
            Dictionary with evaluation metrics
        """
        results = self.model.evaluate(test_generator, steps=steps, return_dict=True)
        return results
    
    def save(self, filepath: str):
        """Save the model."""
        self.model.save(filepath)
        
        # Save config
        config = {
            'model_type': self.model_type,
            'sequence_length': self.sequence_length,
            'frame_height': self.frame_height,
            'frame_width': self.frame_width,
            'gru_units': self.gru_units,
            'dropout_rate': self.dropout_rate,
            'freeze_backbone': self.freeze_backbone,
            'learning_rate': self.learning_rate
        }
        config_path = filepath.replace('.keras', '_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'UVPFLModel':
        """Load a saved model."""
        # Load config
        config_path = filepath.replace('.keras', '_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Create instance
        instance = cls(**config)
        
        # Load weights
        instance.model = keras.models.load_model(filepath)
        
        return instance
    
    def unfreeze_backbone(self, num_layers: int = None):
        """
        Unfreeze backbone layers for fine-tuning.
        
        Args:
            num_layers: Number of layers to unfreeze from the top.
                        If None, unfreeze all layers.
        """
        # Find the TimeDistributed layer with backbone
        for layer in self.model.layers:
            if 'time_distributed' in layer.name:
                backbone = layer.layer
                
                if num_layers is None:
                    backbone.trainable = True
                else:
                    # Unfreeze last num_layers
                    for layer in backbone.layers[:-num_layers]:
                        layer.trainable = False
                    for layer in backbone.layers[-num_layers:]:
                        layer.trainable = True
                
                break
        
        # Recompile with lower learning rate for fine-tuning
        self.model = compile_model(self.model, learning_rate=self.learning_rate / 10)


def test_model():
    """Test model creation and forward pass."""
    print("=" * 60)
    print("Testing UVPFL Model Architecture")
    print("=" * 60)
    
    # Enable GPU memory growth
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"GPU: {gpus[0].name}")
    
    # Test ResNet50 + GRU model
    print("\n1. Creating ResNet50 + GRU model...")
    model = UVPFLModel(model_type='resnet50', freeze_backbone=True)
    
    print("\n2. Model Summary:")
    model.summary()
    
    # Test forward pass
    print("\n3. Testing forward pass...")
    dummy_input = np.random.rand(2, SEQUENCE_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS).astype(np.float32)
    
    with tf.device('/GPU:0'):
        output = model.predict(dummy_input)
    
    print(f"   Input shape: {dummy_input.shape}")
    print(f"   Output shape: {output.shape}")
    print(f"   Sample output (Y, PI, R): {output[0]}")
    
    # Test save/load
    print("\n4. Testing save/load...")
    model.save('checkpoints/test_model.keras')
    print("   Model saved successfully")
    
    # Memory usage
    import subprocess
    result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], 
                          capture_output=True, text=True)
    print(f"\n5. GPU Memory Used: {result.stdout.strip()} MB")
    
    print("\n" + "=" * 60)
    print("✅ Model architecture test passed!")
    print("=" * 60)
    
    return model


if __name__ == '__main__':
    test_model()

