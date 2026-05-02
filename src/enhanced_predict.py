"""
Enhanced Prediction Module with Multi-Model Support, Feature Importance, and SHAP
"""

import numpy as np
import joblib
import os
from sklearn.datasets import load_breast_cancer
from input_validator import InputValidator

class EnhancedPredictor:
    def __init__(self):
        self.models = {}
        self.scaler = None
        self.feature_names = load_breast_cancer().feature_names
        self.best_model_name = None
        self.shap_explainer = None
        self.validator = InputValidator()  # Add input validator
        
    def load_models(self):
        """Load all trained models and SHAP explainer"""
        try:
            # Load all three models
            model_files = {
                'Logistic Regression': 'models/logistic_regression.pkl',
                'Random Forest': 'models/random_forest.pkl',
                'SVM': 'models/svm.pkl'
            }
            
            # Try to load individual models, fallback to best model
            for name, path in model_files.items():
                if os.path.exists(path):
                    self.models[name] = joblib.load(path)
            
            # If individual models don't exist, use best model for all
            if not self.models and os.path.exists('models/best_model.pkl'):
                best_model = joblib.load('models/best_model.pkl')
                self.models['Best Model'] = best_model
                self.best_model_name = 'Best Model'
            
            # Load scaler
            self.scaler = joblib.load('models/scaler.pkl')
            
            # Load SHAP explainer
            try:
                from shap_explainer import get_shap_explainer
                self.shap_explainer = get_shap_explainer()
                print(f"[OK] Loaded {len(self.models)} model(s) with SHAP explainer")
            except Exception as e:
                print(f"[WARNING] SHAP explainer not available: {e}")
                print(f"[OK] Loaded {len(self.models)} model(s)")
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def preprocess_input(self, features):
        """Preprocess input features"""
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        return features_scaled
    
    def predict_all_models(self, features):
        """Make predictions using all models"""
        if not self.models:
            self.load_models()
        
        # Validate input features
        validation_result = self.validator.validate_features(features)
        
        if not validation_result['valid']:
            raise ValueError(f"Invalid input features: {', '.join(validation_result['errors'])}")
        
        # Log warnings if any
        if validation_result['warnings']:
            print("[WARNING] Input validation warnings:")
            for warning in validation_result['warnings']:
                print(f"  - {warning}")
        
        features_scaled = self.preprocess_input(features)
        
        all_predictions = {}
        
        for model_name, model in self.models.items():
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0]
            
            # Apply confidence threshold: if malignant probability is very low, classify as benign
            # This prevents false positives when confidence is extremely low
            if prediction == 1 and probability[1] < 0.5:
                prediction = 0  # Override to benign if malignant confidence < 50%
            
            all_predictions[model_name] = {
                'prediction': int(prediction),
                'prediction_label': 'Malignant' if prediction == 1 else 'Benign',
                'confidence': float(max(probability)),
                'probabilities': {
                    'benign': float(probability[0]),
                    'malignant': float(probability[1])
                }
            }
        
        # Determine consensus
        predictions_list = [p['prediction'] for p in all_predictions.values()]
        consensus = max(set(predictions_list), key=predictions_list.count)
        
        # Get best model (highest confidence)
        best_model = max(all_predictions.items(), key=lambda x: x[1]['confidence'])
        
        result = {
            'all_models': all_predictions,
            'consensus': {
                'prediction': int(consensus),
                'prediction_label': 'Malignant' if consensus == 1 else 'Benign',
                'agreement': predictions_list.count(consensus) / len(predictions_list)
            },
            'best_model': {
                'name': best_model[0],
                'prediction': best_model[1]['prediction'],
                'prediction_label': best_model[1]['prediction_label'],
                'confidence': best_model[1]['confidence']
            }
        }
        
        # Add validation warnings to result if any
        if validation_result['warnings']:
            result['validation_warnings'] = validation_result['warnings']
        
        return result
    
    def get_feature_importance(self, features):
        """Get feature importance for the prediction using SHAP if available"""
        # Try SHAP first (more accurate)
        if self.shap_explainer is not None:
            try:
                # Use Logistic Regression for SHAP (fastest)
                model_name = 'logistic_regression'
                shap_result = self.shap_explainer.explain_prediction(features, model_name)
                
                if shap_result.get('success'):
                    # Convert SHAP top features to our format
                    top_features = []
                    for feat in shap_result['top_features'][:10]:
                        top_features.append({
                            'name': feat['feature'],
                            'importance': feat['abs_shap_value'],
                            'value': feat['value'],
                            'shap_value': feat['shap_value'],
                            'impact': feat['impact']
                        })
                    return top_features
            except Exception as e:
                print(f"SHAP explanation failed, using fallback: {e}")
        
        # Fallback to original method
        features_scaled = self.preprocess_input(features)
        
        # Get feature importance from Random Forest if available
        if 'Random Forest' in self.models:
            model = self.models['Random Forest']
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                
                # Get top 10 most important features
                indices = np.argsort(importances)[-10:][::-1]
                
                top_features = []
                for idx in indices:
                    top_features.append({
                        'name': self.feature_names[idx],
                        'importance': float(importances[idx]),
                        'value': float(features[idx])
                    })
                
                return top_features
        
        # Fallback: use feature values as proxy for importance
        feature_values = np.abs(features_scaled[0])
        indices = np.argsort(feature_values)[-10:][::-1]
        
        top_features = []
        for idx in indices:
            top_features.append({
                'name': self.feature_names[idx],
                'importance': float(feature_values[idx]),
                'value': float(features[idx])
            })
        
        return top_features
    
    def get_shap_explanation(self, features, model_name='logistic_regression'):
        """Get detailed SHAP explanation with visualizations"""
        if self.shap_explainer is None:
            return {'error': 'SHAP explainer not available'}
        
        try:
            return self.shap_explainer.explain_prediction(features, model_name)
        except Exception as e:
            return {'error': str(e)}
    
    def get_risk_assessment(self, prediction, confidence):
        """Assess risk level based on prediction and confidence"""
        if prediction == 0:  # Benign
            if confidence >= 0.9:
                return {'level': 'Low', 'color': 'success', 'message': 'High confidence benign prediction'}
            elif confidence >= 0.7:
                return {'level': 'Low-Medium', 'color': 'info', 'message': 'Moderate confidence benign prediction'}
            else:
                return {'level': 'Medium', 'color': 'warning', 'message': 'Low confidence - recommend further testing'}
        else:  # Malignant
            if confidence >= 0.9:
                return {'level': 'High', 'color': 'danger', 'message': 'High confidence malignant prediction - immediate consultation recommended'}
            elif confidence >= 0.7:
                return {'level': 'Medium-High', 'color': 'warning', 'message': 'Moderate confidence malignant prediction - further testing recommended'}
            else:
                return {'level': 'Medium', 'color': 'warning', 'message': 'Low confidence - comprehensive testing required'}
