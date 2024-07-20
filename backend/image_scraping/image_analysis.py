import cv2
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from keras.preprocessing.image import img_to_array
from sklearn.cluster import KMeans
import os

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

def classify_image(image_path):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error loading image: {image_path}")
        return "Unknown"
    
    # Resize image to 224x224 pixels as required by MobileNetV2
    img_resized = cv2.resize(img, (224, 224))
    
    # Convert image to array and preprocess it for the model
    img_array = img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Make predictions
    predictions = model.predict(img_array)
    label = decode_predictions(predictions)
    
    # Extract the most likely label
    label = label[0][0][1]
    
    # Classify based on the label
    if any(word in label for word in ['dress', 'gown', 'robe']):
        return "Dress"
    elif any(word in label for word in ['trouser', 'jeans', 'pants', 'shorts', 'skirt']):
        return "Lower Wear"
    elif any(word in label for word in ['shirt', 'blouse', 'top', 't-shirt', 'jacket', 'coat', 'sweater']):
        return "Upper Wear"
    else:
        return "Other"

def extract_dominant_colors(image_path, num_colors=3):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error loading image: {image_path}")
        return []

    # Convert image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape the image to be a list of pixels
    img_rgb = img_rgb.reshape((img_rgb.shape[0] * img_rgb.shape[1], 3))

    # Perform k-means clustering to find the most dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(img_rgb)
    colors = kmeans.cluster_centers_
    
    return colors.astype(int).tolist()

def process_images(image_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            
            # Classify image type (lower wear, upper wear, dress)
            category = classify_image(image_path)
            
            # Extract dominant colors
            colors = extract_dominant_colors(image_path, num_colors=3)
            
            # Print or store results
            print(f"Image: {filename}")
            print(f"Category: {category}")
            print(f"Dominant Colors RGB Values:")
            print(colors)
            print("-----------------------------")