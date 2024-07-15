# Trend Tailors

Trend Tailors is a web application that allows users to upload images of their wardrobe items along with associated details such as wear type, style category, brand name, color, item name, and gender. The application processes the uploaded images, stores the metadata in a database, performs trend analysis, and provides recommendations for matching items based on trends and popularity.

## Features

- **Image Upload**: Users can upload images of their wardrobe items.
- **Image Processing**: Uploaded images are processed and stored.
- **Metadata Storage**: Associated details (wear type, style category, brand name, color, item name, and gender) are stored in a database.
- **Product Recommendations**: Based on the wear type of the selected product, the system recommends related products from a CSV dataset.
- **Product Listing**: Displays recommended products with their images and details.
- **Trend Analysis**: Analyzes trends based on user-uploaded images and  data to recommend trending items.

## Project Structure

- **Backend**: Flask server for handling image uploads, processing, and providing API endpoints.
- **Frontend**: React application for the user interface.
- **Database**: SQLite database for storing image metadata.
- **CSV Dataset**: Used for recommending products.
- **Trend Analysis**: Python scripts for analyzing trends based on user-uploaded images and social media data.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/menavipandey/Trend_Tailors.git
   cd Trend_Tailors
2. **Backend Setup and run**
   * Ensure you have Python installed.
   * Navigate to the backend directory.
     ```bash
     cd backend
   * Install the required Python packages:
     ```bash
     pip install -r requirements.txt
   * Run the Flask server:
     ```bash
     python app.py
3. Frontend Setup and run:
   * Ensure you have Node.js and npm installed.
   * Navigate to the frontend directory:
   * ```bash
     cd ../frontend
   * Run the React development server:
     ```bash
     npm start

## Usage

### Uploading an Image:

- Use the upload form to upload an image along with its associated details.
- The image will be processed and stored on the server, and the details will be saved in the database.

### Viewing Image Details:

- Navigate to the image details page by selecting an uploaded image.
- View the details of the uploaded image.

### Product Recommendations:

- View recommended products based on the wear type and other attributes of the selected image.

### Trend Analysis:

- The system analyzes trends based on user-uploaded images and social media data.
- Recommends trending items accordingly.

## API Endpoints

- **Upload Image**: `POST /upload`
- **Get Image Details**: `GET /image-details/:image_id`
- **Get Recommended Products**: `GET /recommended-products?product_id=:product_id`
- **Fetch Image**: `GET /uploads/:filename`

## Technologies Used

- **Frontend**: React, Axios, CSS
- **Backend**: Flask, SQLite,python , OpenCV, TensorFlow , pandas , numpy
- **Dataset**: Ecommerce-shopping products dataset 
  




