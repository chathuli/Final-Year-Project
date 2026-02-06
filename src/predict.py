"""
Prediction Module for Breast Cancer Detection
Loads trained model and makes predictions
"""

import numpy as np
import joblib
import os

class BreastCancerPredictor:
    def __init__(self, model_path='models/best_model.pkl', scaler_path='models/scaler.pkl'):
        self.model = None
        self.scaler = None
        self.model_path = model_path
        self.scaler_path = scaler_path
        
    def load_model(self):
        """Load trained model and scaler"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print("Model and scaler loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def preprocess_input(self, features):
        """Preprocess input features"""
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        return features_scaled
    
    def predict(self, features):
        """Make prediction"""
        if self.model is None:
            self.load_model()
        
        # Preprocess features
        features_scaled = self.preprocess_input(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        # prediction: 0 = Benign, 1 = Malignant
        result = {
            'prediction': int(prediction),
            'confidence': float(max(probability)),
            'probabilities': {
                'benign': float(probability[0]),
                'malignant': float(probability[1])
            }
        }
        
        return result

if __name__ == "__main__":
    # Example usage
    predictor = BreastCancerPredictor()
    predictor.load_model()
