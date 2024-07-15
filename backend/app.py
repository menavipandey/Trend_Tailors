from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import cv2
import numpy as np
import tensorflow as tf
import sqlite3
import pandas as pd

df = pd.read_csv('../services/new2.csv')

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PRODUCTS_FOLDER = 'products' 
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PRODUCTS_FOLDER):
    os.makedirs(PRODUCTS_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PRODUCTS_FOLDER'] = PRODUCTS_FOLDER

def process_image(filepath):
    try:
        image = cv2.imread(filepath)
        resized_image = cv2.resize(image, (224, 224))
        tensor = tf.convert_to_tensor(resized_image, dtype=tf.float32)
        normalized_tensor = tensor / 255.0
        return {
            'shape': normalized_tensor.shape.as_list(),
            'data': normalized_tensor.numpy().tolist()
        }
    except Exception as e:
        print(f'Error processing image: {e}')
        raise e

def store_image_data(filename, wear_type, style_category, brand_name, color, item_name, gender):
    conn = sqlite3.connect('image_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO image_data (filename, wearType, styleCategory, brandName, color, itemName, Gender)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (filename, wear_type, style_category, brand_name, color, item_name, gender))
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Upload request received")
    if 'image' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    wear_type = request.form.get('wearType')
    style_category = request.form.get('styleCategory')
    brand_name = request.form.get('brandName')
    color = request.form.get('color')
    item_name = request.form.get('itemName')
    gender = request.form.get('gender') 

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        print(f"File saved to {filepath}")
        processed_data = process_image(filepath)
        print(f"Image processed: {processed_data}")
        store_image_data(filename, wear_type, style_category, brand_name, color, item_name, gender)
        return jsonify({'message': 'File uploaded successfully!', 'data': processed_data}), 200
    except Exception as e:
        print(f'Error processing file: {e}')
        return jsonify({'error': 'Error processing file.'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/products/<filename>')
def product_file(filename):
    return send_from_directory(app.config['PRODUCTS_FOLDER'], filename)

@app.route('/images', methods=['GET'])
def get_images():
    try:
        images = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(images)
    except Exception as e:
        print(f'Error fetching images: {e}')
        return jsonify({'error': 'Error fetching images.'}), 500

@app.route('/recommended-products', methods=['GET'])
def get_recommended_products():
    try:
        product_id = request.args.get('product_id')
        if not product_id:
            return jsonify({'error': 'Product ID parameter is required.'}), 400

        # Fetch wear type and gender of the selected product
        conn = sqlite3.connect('image_data.db')
        c = conn.cursor()
        c.execute('SELECT wearType, Gender FROM image_data WHERE filename = ?', (product_id,))
        row = c.fetchone()
        if not row:
            return jsonify({'error': 'Product not found.'}), 404
        
        wear_type = row[0]
        gender = row[1]

        # Fetch recommended products based on wear type, gender, popularity, and excluding unknown values
        recommended_products = df[(df['wearCategory'] != wear_type) & 
                                  (df['Gender'] == gender) &
                                  (df['Popularity'] > 0) &
                                  (df['wearCategory'] != 'unknown') & 
                                  (df['StyleCategory'] != 'Unknown')]
        
        # Sort recommended products by Popularity in descending order
        recommended_products = recommended_products.sort_values(by='Popularity', ascending=False).head(10)

        # Convert to dictionary format
        recommended_products = recommended_products.to_dict(orient='records')

        # Add image URLs to each recommended product
        for product in recommended_products:
            product_id = product['ProductID']  # Assuming this matches the filename in products directory
            product['image_url'] = f'http://localhost:5000/products/{product_id}.png'  

        conn.close()

        return jsonify(recommended_products)
    
    except Exception as e:
        print(f'Error fetching recommended products: {e}')
        return jsonify({'error': 'Error fetching recommended products.'}), 500

@app.route('/image-details/<image_id>', methods=['GET'])
def get_image_details(image_id):
    try:
        conn = sqlite3.connect('image_data.db')
        c = conn.cursor()
        c.execute('SELECT filename, wearType, styleCategory, brandName, color, itemName FROM image_data WHERE filename = ?', (image_id,))
        row = c.fetchone()
        conn.close()

        if row:
            image_details = {
                'itemType': row[5],
                'brand': row[3],
                'wearType': row[1],
                'styleCategory': row[2],
                'color': row[4] 
            }
            return jsonify(image_details)
        else:
            return jsonify({'error': 'Image details not found'}), 404
    except Exception as e:
        print(f'Error fetching image details: {e}')
        return jsonify({'error': 'Error fetching image details.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
