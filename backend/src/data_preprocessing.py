from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(data_dir, img_size=(128, 128), batch_size=32, validation_split=0.1):
    datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=validation_split
    )

    train_generator = datagen.flow_from_directory(
        f'{data_dir}/TRAIN',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        color_mode='grayscale',
        subset='training'
    )

    validation_generator = datagen.flow_from_directory(
        f'{data_dir}/TRAIN',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        color_mode='grayscale',
        subset='validation'
    )

    return train_generator, validation_generator
