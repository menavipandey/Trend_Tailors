import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './productDetails.css';

function ProductDetail() {
    const { id } = useParams();
    const [imageDetails, setImageDetails] = useState({});
    const [recommendedProducts, setRecommendedProducts] = useState([]);

    useEffect(() => {
        fetchImageDetails(id);
    }, [id]);

    const fetchImageDetails = async (imageId) => {
        try {
            const response = await axios.get(`http://localhost:5000/image-details/${imageId}`);
            setImageDetails(response.data);
            fetchRecommendedProducts(response.data.wearType);
        } catch (error) {
            console.error('Error fetching image details:', error);
        }
    };

    const fetchRecommendedProducts = async (wearType) => {
        try {
            const response = await axios.get(`http://localhost:5000/recommended-products?product_id=${id}`);
            setRecommendedProducts(response.data);
        } catch (error) {
            console.error('Error fetching recommended products:', error);
        }
    };

    return (
        <div className="product-detail-container">
            <div className="image-section">
                <img
                    src={`http://localhost:5000/uploads/${id}`}
                    alt={id}
                    className="detailed-image"
                    onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = 'placeholder-image-url';
                    }}
                />
                <div className="image-details">
                    <h2>{imageDetails.itemName}</h2>
                    <p>Brand: {imageDetails.brand}</p>
                    <p>Wear Type: {imageDetails.wearType}</p>
                    <p>Style Category: {imageDetails.styleCategory}</p>
                    <p>Color: {imageDetails.color}</p>
                </div>
            </div>
            <div className="recommended-section">
                <h2>Recommended Products</h2>
                <div className="recommended-products">
                    {recommendedProducts.length > 0 ? (
                        recommendedProducts.map((product, index) => (
                            <div key={index} className="product-card">
                                <div className="product-thumb">
                                    <img src={product.image_url} alt={product.ProductName} />
                                </div>
                                <div className="product-details">
                                    <span className="product-category">{product.ProductBrand}</span>
                                    <h4><a href="#">{product.ProductName}</a></h4>
                                    <p>Color: {product.PrimaryColor}</p>
                                    <div className="product-bottom-details">
                                        {/* <div className="product-price">{product['Price (INR)']} INR</div> */}
                                        <div className="product-links">
                                            <a href="#">Buy Now</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>No recommended products available.</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ProductDetail;
