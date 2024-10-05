import cv2  # Import OpenCV
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('models/saved_model.keras')

def predict_image_opencv(img, model):
    # Preprocess the image (resize to 128x128 as expected by the model)
    img_resized = cv2.resize(img, (128, 128))
    
    # Normalize pixel values (convert from [0, 255] to [0, 1])
    img_normalized = img_resized / 255.0
    
    # Expand dimensions to match the input shape expected by the model (1, 128, 128, 3)
    img_expanded = np.expand_dims(img_normalized, axis=0)
    
    # Make predictions
    prediction = model.predict(img_expanded)
    
    # Get the class index with the highest predicted probability
    class_idx = np.argmax(prediction)
    
    # Map the class index to the corresponding label (assuming class labels: Non-Recyclable, Organic, Recyclable)
    class_labels = ['Non_Recyclable', 'Organic', 'Recyclable']
    predicted_class = class_labels[class_idx]
    
    return predicted_class

def capture_image_from_webcam():
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    print("Press 'Space' to capture an image, 'Esc' to exit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Display the frame in a window
        cv2.imshow('Webcam', frame)
        
        # Wait for user input
        key = cv2.waitKey(1)
        
        if key == 27:  # ESC key to break
            print("Exiting...")
            break
        elif key == 32:  # Space key to capture the image
            print("Image captured.")
            captured_image = frame
            break
    
    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

    return captured_image

# Capture an image from the webcam
captured_image = capture_image_from_webcam()

if captured_image is not None:
    # Make prediction using the captured image
    predicted_class = predict_image_opencv(captured_image, model)
    
    # Print the predicted class
    print(f'Predicted class: {predicted_class}')
else:
    print("No image captured.")
