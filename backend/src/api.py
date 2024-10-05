from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load your saved model
model = load_model('models/saved_model.keras')

# Preprocess image for the model
def preprocess_image(image: Image.Image):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    # Resize image to 128x128
    image = cv2.resize(image, (128, 128))
    # Normalize pixel values to [0, 1]
    image = image / 255.0
    # Expand dimensions to match the input shape (1, 128, 128, 3)
    image = np.expand_dims(image, axis=0)
    return image

# Endpoint to handle image upload and prediction
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image bytes from uploaded file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Preprocess image
    processed_image = preprocess_image(image)
    
    # Make prediction
    prediction = model.predict(processed_image)
    class_idx = np.argmax(prediction)
    class_labels = ['Non_Recyclable', 'Organic', 'Recyclable']
    predicted_class = class_labels[class_idx]
    
    return {"predicted_class": predicted_class}

