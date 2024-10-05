from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model
model = load_model('models/saved_model.keras')

def predict_image(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)

    class_labels = ['N', 'O', 'R']
    return class_labels[class_idx]

# Test on a new image
img_path = input("Enter path: " )  # Path to your test image
predicted_class = predict_image(img_path, model)
print(f'Predicted class: {predicted_class}')
