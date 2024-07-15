import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);
    const [images, setImages] = useState([]);
    const [wearType, setWearType] = useState('');
    const [styleCategory, setStyleCategory] = useState('');
    const [brandName, setBrandName] = useState('');
    const [color, setColor] = useState('');
    const [itemName, setItemName] = useState('');
    const [gender, setGender] = useState('');
    useEffect(() => {
        fetchImages();
    }, []);

    const fetchImages = async () => {
        try {
            const response = await axios.get('http://localhost:5000/images');
            setImages(response.data);
        } catch (error) {
            console.error('Error fetching images:', error);
        }
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setUploadedImage(URL.createObjectURL(selectedFile));
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a file.');
            return;
        }

        setUploading(true);
        setMessage('');

        const formData = new FormData();
        formData.append('image', file);
        formData.append('wearType', wearType);
        formData.append('styleCategory', styleCategory);
        formData.append('brandName', brandName);
        formData.append('color', color);
        formData.append('itemName', itemName); 
        formData.append('gender', gender); 

        try {
            const res = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(res.data);
            setMessage('File uploaded successfully!');
            setFile(null);
            setUploadedImage(null);
            setWearType('');
            setStyleCategory('');
            setBrandName('');
            setColor('');
            setItemName('');
            setGender('');
            fetchImages();
        } catch (err) {
            console.error('Error uploading file:', err);
            setMessage('Error uploading file. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Upload Your Wardrobe Image</h1>
            </header>
            <div className="upload-container">
                <input type="file" onChange={handleFileChange} />
                <input
                    type="text"
                    placeholder="Wear Type"
                    value={wearType}
                    onChange={(e) => setWearType(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Style Category"
                    value={styleCategory}
                    onChange={(e) => setStyleCategory(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Brand Name"
                    value={brandName}
                    onChange={(e) => setBrandName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Color"
                    value={color}
                    onChange={(e) => setColor(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Item Name" // New input field
                    value={itemName}
                    onChange={(e) => setItemName(e.target.value)}
                />
                 <input
                    type="text"
                    placeholder="Gender" // New input field for gender
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                />
                <button onClick={handleUpload} disabled={uploading}>
                    {uploading ? 'Uploading...' : 'Upload'}
                </button>
            </div>
            {message && <p className="message">{message}</p>}
            {uploadedImage && (
                <div className="preview-container">
                    <h2>Preview</h2>
                    <img src={uploadedImage} alt="Uploaded" className="preview-image" />
                </div>
            )}
            <h2>Uploaded Images</h2>
            <div className="images-container">
                {images.length > 0 ? (
                    images.map((image) => (
                        <Link key={image} to={`/product/${image}`} className="image-item">
                            <img
                                src={`http://localhost:5000/uploads/${image}`}
                                alt={image}
                                className="uploaded-image"
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = 'placeholder-image-url';
                                }}
                            />
                        </Link>
                    ))
                ) : (
                    <p>No images uploaded yet.</p>
                )}
            </div>
        </div>
    );
}

export default Home;
