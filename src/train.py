import os
from data_preprocessing import create_data_generators
from model import create_cnn_model
from tensorflow.keras.callbacks import ModelCheckpoint

# Directory for saving models
MODEL_DIR = 'models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Data directories
data_dir = 'DATASET'

# Parameters
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 20

# Create data generators
train_generator, validation_generator = create_data_generators(data_dir, IMG_SIZE, BATCH_SIZE)

# Create model
model = create_cnn_model(input_shape=(128, 128, 1), num_classes=3)

# Save model checkpoint
checkpoint = ModelCheckpoint(os.path.join(MODEL_DIR, 'saved_model3.keras'), save_best_only=True)

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=EPOCHS,
    callbacks=[checkpoint]
)
