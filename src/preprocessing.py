"""
Data Preprocessing Module for Breast Cancer Detection
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def load_data(self, filepath):
        """Load dataset from file"""
        try:
            data = pd.read_csv(filepath)
            print(f"Data loaded successfully. Shape: {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self, data):
        """Clean and prepare data"""
        # Remove duplicates
        data = data.drop_duplicates()
        
        # Handle missing values
        data = data.fillna(data.mean(numeric_only=True))
        
        # Remove unnecessary columns if any
        if 'id' in data.columns:
            data = data.drop('id', axis=1)
        
        return data
    
    def encode_target(self, data, target_column='diagnosis'):
        """Encode target variable (M=1, B=0)"""
        if target_column in data.columns:
            # Check if already numeric
            if data[target_column].dtype in ['int64', 'float64']:
                # Already numeric, no encoding needed
                pass
            else:
                # Encode string values
                data[target_column] = data[target_column].map({'M': 1, 'B': 0})
        return data
    
    def split_features_target(self, data, target_column='diagnosis'):
        """Split data into features and target"""
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        return X, y
    
    def scale_features(self, X_train, X_test):
        """Scale features using StandardScaler"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def prepare_data(self, filepath, test_size=0.2, random_state=42):
        """Complete data preparation pipeline"""
        # Load data
        data = self.load_data(filepath)
        if data is None:
            return None
        
        # Clean data
        data = self.clean_data(data)
        
        # Encode target
        data = self.encode_target(data)
        
        # Split features and target
        X, y = self.split_features_target(data)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        print(f"Training set size: {X_train_scaled.shape}")
        print(f"Test set size: {X_test_scaled.shape}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    # Example usage
    # X_train, X_test, y_train, y_test = preprocessor.prepare_data('data/breast_cancer.csv')
