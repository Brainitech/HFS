from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import random
import os
import cv2

# Load the trained model
model = load_model('models/saved_model.keras')

def predict_image(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)

    class_labels = ['Non-Recyclable', 'Organic', 'Recyclable']
    return class_labels[class_idx]

# Test on a new image

img_path =random.choice([
    'data/DATASET/TEST/R/' + random.choice(os.listdir('data/DATASET/TEST/R')),
    'data/DATASET/TEST/N/' + random.choice(os.listdir('data/DATASET/TEST/N')),
    'data/DATASET/TEST/O/' + random.choice(os.listdir('data/DATASET/TEST/O'))
])

#img_path= 'Untitled.jpg'
cv2.imshow('Image', cv2.imread(img_path))
cv2.waitKey(0)
cv2.destroyAllWindows()

predicted_class = predict_image(img_path, model)
print(f'Predicted class: {predicted_class}')
