"""
Image Analysis Module for Breast Cancer Detection
Analyzes mammogram images and provides predictions
"""

import os
import numpy as np
from PIL import Image
import io

class ImageAnalyzer:
    """Analyzes medical images for breast cancer detection"""
    
    def __init__(self):
        """Initialize the image analyzer"""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.image_size = (224, 224)
    
    def validate_image(self, image_file):
        """
        Validate uploaded image
        
        Args:
            image_file: File object from request
            
        Returns:
            dict: Validation result
        """
        try:
            # Check file extension
            filename = image_file.filename.lower()
            ext = os.path.splitext(filename)[1]
            
            if ext not in self.supported_formats:
                return {
                    'valid': False,
                    'error': f'Unsupported format. Please upload: {", ".join(self.supported_formats)}'
                }
            
            # Try to open image
            image = Image.open(image_file)
            
            # Check image mode
            if image.mode not in ['RGB', 'L', 'RGBA']:
                return {
                    'valid': False,
                    'error': 'Invalid image mode. Please upload a valid medical image.'
                }
            
            # Check image size
            if image.size[0] < 50 or image.size[1] < 50:
                return {
                    'valid': False,
                    'error': 'Image too small. Minimum size: 50x50 pixels'
                }
            
            return {
                'valid': True,
                'image': image,
                'size': image.size,
                'mode': image.mode
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error reading image: {str(e)}'
            }
    
    def preprocess_image(self, image):
        """
        Preprocess image for analysis
        
        Args:
            image: PIL Image object
            
        Returns:
            numpy array: Preprocessed image
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to standard size
        image = image.resize(self.image_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Normalize pixel values
        img_array = img_array / 255.0
        
        return img_array
    
    def extract_features(self, img_array):
        """
        Extract features from preprocessed image
        This is a simplified feature extraction
        In production, you would use a CNN model
        
        Args:
            img_array: Preprocessed image array
            
        Returns:
            list: 30 features for Wisconsin dataset compatibility
        """
        # Calculate basic image statistics
        mean_r = np.mean(img_array[:, :, 0])
        mean_g = np.mean(img_array[:, :, 1])
        mean_b = np.mean(img_array[:, :, 2])
        
        std_r = np.std(img_array[:, :, 0])
        std_g = np.std(img_array[:, :, 1])
        std_b = np.std(img_array[:, :, 2])
        
        # Convert to grayscale for texture analysis
        gray = np.mean(img_array, axis=2)
        
        # Calculate texture features
        texture_mean = np.mean(gray)
        texture_std = np.std(gray)
        texture_max = np.max(gray)
        texture_min = np.min(gray)
        
        # Calculate edge features (simplified gradient)
        grad_x = np.gradient(gray, axis=1)
        grad_y = np.gradient(gray, axis=0)
        edge_strength = np.sqrt(grad_x**2 + grad_y**2)
        
        edge_mean = np.mean(edge_strength)
        edge_std = np.std(edge_strength)
        edge_max = np.max(edge_strength)
        
        # Map to 30 features (Wisconsin dataset format)
        # This is a simplified mapping - in production use CNN features
        features = [
            texture_mean * 20,      # radius_mean
            texture_std * 15,       # texture_mean
            edge_mean * 100,        # perimeter_mean
            texture_mean * 500,     # area_mean
            edge_std * 0.1,         # smoothness_mean
            texture_std * 0.2,      # compactness_mean
            edge_mean * 0.15,       # concavity_mean
            edge_std * 0.1,         # concave_points_mean
            mean_r * 0.2,           # symmetry_mean
            std_r * 0.3,            # fractal_dimension_mean
            texture_mean * 0.5,     # radius_se
            texture_std * 0.8,      # texture_se
            edge_mean * 2,          # perimeter_se
            texture_mean * 30,      # area_se
            edge_std * 0.01,        # smoothness_se
            texture_std * 0.02,     # compactness_se
            edge_mean * 0.02,       # concavity_se
            edge_std * 0.01,        # concave_points_se
            mean_g * 0.02,          # symmetry_se
            std_g * 0.003,          # fractal_dimension_se
            texture_max * 25,       # radius_worst
            texture_std * 20,       # texture_worst
            edge_max * 150,         # perimeter_worst
            texture_max * 800,      # area_worst
            edge_std * 0.15,        # smoothness_worst
            texture_std * 0.4,      # compactness_worst
            edge_mean * 0.4,        # concavity_worst
            edge_max * 0.15,        # concave_points_worst
            mean_b * 0.3,           # symmetry_worst
            std_b * 0.08            # fractal_dimension_worst
        ]
        
        return features
    
    def analyze_image(self, image_file):
        """
        Complete image analysis pipeline
        
        Args:
            image_file: File object from request
            
        Returns:
            dict: Analysis result with features
        """
        # Validate image
        validation = self.validate_image(image_file)
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['error']
            }
        
        # Preprocess image
        img_array = self.preprocess_image(validation['image'])
        
        # Extract features
        features = self.extract_features(img_array)
        
        return {
            'success': True,
            'features': features,
            'image_info': {
                'original_size': validation['size'],
                'processed_size': self.image_size,
                'mode': validation['mode']
            }
        }
    
    def get_image_quality_score(self, img_array):
        """
        Calculate image quality score
        
        Args:
            img_array: Image array
            
        Returns:
            dict: Quality metrics
        """
        # Calculate sharpness (edge strength)
        gray = np.mean(img_array, axis=2)
        grad_x = np.gradient(gray, axis=1)
        grad_y = np.gradient(gray, axis=0)
        sharpness = np.mean(np.sqrt(grad_x**2 + grad_y**2))
        
        # Calculate contrast
        contrast = np.std(gray)
        
        # Calculate brightness
        brightness = np.mean(gray)
        
        # Overall quality score (0-100)
        quality_score = min(100, (sharpness * 100 + contrast * 50 + brightness * 30) / 1.8)
        
        return {
            'quality_score': round(quality_score, 2),
            'sharpness': round(sharpness, 4),
            'contrast': round(contrast, 4),
            'brightness': round(brightness, 4)
        }
