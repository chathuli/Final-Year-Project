"""
Model Training Module for Breast Cancer Detection
Trains and evaluates multiple ML models
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import os
from preprocessing import DataPreprocessor

class ModelTrainer:
    def __init__(self):
        self.models = {
            'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'svm': SVC(kernel='rbf', probability=True, random_state=42)
        }
        self.best_model = None
        self.best_model_name = None
        self.best_score = 0
        
    def train_model(self, model, X_train, y_train):
        """Train a single model"""
        model.fit(X_train, y_train)
        return model
    
    def evaluate_model(self, model, X_test, y_test):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred)
        }
        
        return metrics, y_pred
    
    def train_all_models(self, X_train, X_test, y_train, y_test):
        """Train and evaluate all models"""
        results = {}
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            trained_model = self.train_model(model, X_train, y_train)
            
            # Evaluate model
            metrics, y_pred = self.evaluate_model(trained_model, X_test, y_test)
            
            # Store results
            results[name] = {
                'model': trained_model,
                'metrics': metrics,
                'predictions': y_pred
            }
            
            # Print results
            print(f"{name} Results:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")
            
            # Track best model
            if metrics['accuracy'] > self.best_score:
                self.best_score = metrics['accuracy']
                self.best_model = trained_model
                self.best_model_name = name
            
            # Save individual model
            model_filename = name.lower().replace(' ', '_') + '.pkl'
            self.save_model(trained_model, model_filename)
        
        print(f"\nBest Model: {self.best_model_name} with accuracy: {self.best_score:.4f}")
        return results
    
    def save_model(self, model, filename):
        """Save trained model"""
        os.makedirs('models', exist_ok=True)
        filepath = os.path.join('models', filename)
        joblib.dump(model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filename):
        """Load trained model"""
        filepath = os.path.join('models', filename)
        model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
        return model

def main():
    """Main training pipeline"""
    print("Starting Breast Cancer Detection Model Training...")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Prepare data
    print("\nPreparing data...")
    data_path = 'data/breast_cancer.csv'
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(data_path)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Train all models
    print("\nTraining models...")
    results = trainer.train_all_models(X_train, X_test, y_train, y_test)
    
    # Save best model
    trainer.save_model(trainer.best_model, 'best_model.pkl')
    trainer.save_model(preprocessor.scaler, 'scaler.pkl')
    
    print("\nTraining completed successfully!")

if __name__ == "__main__":
    main()
