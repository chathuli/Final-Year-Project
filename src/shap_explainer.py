"""
SHAP (SHapley Additive exPlanations) Explainer Module
Provides advanced model interpretability using SHAP values
"""

import shap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from pathlib import Path
import joblib

class SHAPExplainer:
    """
    SHAP-based model explainer for breast cancer detection
    Provides detailed explanations of model predictions
    """
    
    def __init__(self, models_dir='models'):
        self.models_dir = Path(models_dir)
        self.models = {}
        self.explainers = {}
        self.feature_names = [
            'mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area',
            'mean_smoothness', 'mean_compactness', 'mean_concavity',
            'mean_concave_points', 'mean_symmetry', 'mean_fractal_dimension',
            'radius_error', 'texture_error', 'perimeter_error', 'area_error',
            'smoothness_error', 'compactness_error', 'concavity_error',
            'concave_points_error', 'symmetry_error', 'fractal_dimension_error',
            'worst_radius', 'worst_texture', 'worst_perimeter', 'worst_area',
            'worst_smoothness', 'worst_compactness', 'worst_concavity',
            'worst_concave_points', 'worst_symmetry', 'worst_fractal_dimension'
        ]
        
    def load_models(self):
        """Load trained models and create SHAP explainers"""
        try:
            # Load models
            self.models['logistic_regression'] = joblib.load(
                self.models_dir / 'logistic_regression.pkl'
            )
            self.models['random_forest'] = joblib.load(
                self.models_dir / 'random_forest.pkl'
            )
            self.models['svm'] = joblib.load(
                self.models_dir / 'svm.pkl'
            )
            
            # Load scaler
            self.scaler = joblib.load(self.models_dir / 'scaler.pkl')
            
            # Load background data for SHAP
            self._load_background_data()
            
            # Create SHAP explainers for each model
            self._create_explainers()
            
            print(f"[OK] Loaded {len(self.models)} models with SHAP explainers")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def _load_background_data(self):
        """Load background data for SHAP explainers"""
        try:
            # Load training data for background
            import pandas as pd
            data_path = Path('data/breast_cancer.csv')
            
            if data_path.exists():
                df = pd.read_csv(data_path)
                
                # Remove non-feature columns
                feature_cols = [col for col in df.columns 
                               if col not in ['id', 'diagnosis']]
                
                X = df[feature_cols].values
                
                # Scale the data
                X_scaled = self.scaler.transform(X)
                
                # Use a sample for background (100 samples for speed)
                self.background_data = shap.sample(X_scaled, 100)
                
                print(f"[OK] Loaded background data: {self.background_data.shape}")
            else:
                # Create synthetic background data if file doesn't exist
                self.background_data = np.random.randn(100, 30)
                print("[WARNING] Using synthetic background data")
                
        except Exception as e:
            print(f"Warning: Could not load background data: {e}")
            # Fallback to synthetic data
            self.background_data = np.random.randn(100, 30)
    
    def _create_explainers(self):
        """Create SHAP explainers for each model"""
        try:
            # Logistic Regression - use Linear explainer
            self.explainers['logistic_regression'] = shap.LinearExplainer(
                self.models['logistic_regression'],
                self.background_data
            )
            
            # Random Forest - use Tree explainer
            self.explainers['random_forest'] = shap.TreeExplainer(
                self.models['random_forest']
            )
            
            # SVM - use Kernel explainer (slower but works for any model)
            self.explainers['svm'] = shap.KernelExplainer(
                self.models['svm'].predict_proba,
                self.background_data
            )
            
            print(f"[OK] Created {len(self.explainers)} SHAP explainers")
            
        except Exception as e:
            print(f"Error creating explainers: {e}")
    
    def explain_prediction(self, features, model_name='logistic_regression'):
        """
        Generate SHAP explanation for a single prediction
        
        Args:
            features: Array of 30 feature values
            model_name: Name of the model to explain
            
        Returns:
            Dictionary with SHAP values and visualizations
        """
        try:
            # Ensure features is 2D array
            if len(np.array(features).shape) == 1:
                features = np.array(features).reshape(1, -1)
            
            # Get the explainer
            explainer = self.explainers.get(model_name)
            if explainer is None:
                return {'error': f'No explainer for {model_name}'}
            
            # Calculate SHAP values
            if model_name == 'random_forest':
                shap_values = explainer.shap_values(features)
                # For binary classification, take the positive class
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
            else:
                shap_values = explainer.shap_values(features)
                if len(shap_values.shape) > 2:
                    shap_values = shap_values[:, :, 1]
            
            # Get base value (expected value)
            if hasattr(explainer, 'expected_value'):
                expected_value = explainer.expected_value
                if isinstance(expected_value, np.ndarray):
                    expected_value = expected_value[1] if len(expected_value) > 1 else expected_value[0]
            else:
                expected_value = 0.5
            
            # Create explanation object
            explanation = shap.Explanation(
                values=shap_values[0],
                base_values=expected_value,
                data=features[0],
                feature_names=self.feature_names
            )
            
            # Generate visualizations
            force_plot = self._generate_force_plot(explanation)
            waterfall_plot = self._generate_waterfall_plot(explanation)
            
            # Get top features
            top_features = self._get_top_features(shap_values[0], features[0])
            
            return {
                'success': True,
                'shap_values': shap_values[0].tolist(),
                'expected_value': float(expected_value),
                'top_features': top_features,
                'force_plot': force_plot,
                'waterfall_plot': waterfall_plot,
                'feature_names': self.feature_names
            }
            
        except Exception as e:
            print(f"Error explaining prediction: {e}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _generate_force_plot(self, explanation):
        """Generate SHAP force plot as base64 image"""
        try:
            plt.figure(figsize=(20, 3))
            shap.plots.force(explanation, matplotlib=True, show=False)
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"Error generating force plot: {e}")
            return None
    
    def _generate_waterfall_plot(self, explanation):
        """Generate SHAP waterfall plot as base64 image"""
        try:
            plt.figure(figsize=(10, 8))
            shap.plots.waterfall(explanation, show=False)
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"Error generating waterfall plot: {e}")
            return None
    
    def _get_top_features(self, shap_values, feature_values, top_n=10):
        """Get top contributing features based on absolute SHAP values"""
        # Get absolute SHAP values
        abs_shap = np.abs(shap_values)
        
        # Get indices of top features
        top_indices = np.argsort(abs_shap)[-top_n:][::-1]
        
        # Create list of top features
        top_features = []
        for idx in top_indices:
            top_features.append({
                'feature': self.feature_names[idx],
                'value': float(feature_values[idx]),
                'shap_value': float(shap_values[idx]),
                'abs_shap_value': float(abs_shap[idx]),
                'impact': 'Increases risk' if shap_values[idx] > 0 else 'Decreases risk'
            })
        
        return top_features
    
    def generate_summary_plot(self, X_sample, model_name='logistic_regression'):
        """
        Generate SHAP summary plot for multiple predictions
        
        Args:
            X_sample: Array of samples (n_samples, 30)
            model_name: Name of the model
            
        Returns:
            Base64 encoded image
        """
        try:
            explainer = self.explainers.get(model_name)
            if explainer is None:
                return None
            
            # Calculate SHAP values
            if model_name == 'random_forest':
                shap_values = explainer.shap_values(X_sample)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
            else:
                shap_values = explainer.shap_values(X_sample)
                if len(shap_values.shape) > 2:
                    shap_values = shap_values[:, :, 1]
            
            # Generate summary plot
            plt.figure(figsize=(10, 8))
            shap.summary_plot(
                shap_values,
                X_sample,
                feature_names=self.feature_names,
                show=False
            )
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"Error generating summary plot: {e}")
            return None
    
    def get_feature_importance(self, model_name='logistic_regression'):
        """
        Get global feature importance based on mean absolute SHAP values
        
        Args:
            model_name: Name of the model
            
        Returns:
            List of features sorted by importance
        """
        try:
            # Use background data to calculate importance
            explainer = self.explainers.get(model_name)
            if explainer is None:
                return []
            
            # Calculate SHAP values for background data
            if model_name == 'random_forest':
                shap_values = explainer.shap_values(self.background_data)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
            else:
                shap_values = explainer.shap_values(self.background_data)
                if len(shap_values.shape) > 2:
                    shap_values = shap_values[:, :, 1]
            
            # Calculate mean absolute SHAP values
            mean_abs_shap = np.abs(shap_values).mean(axis=0)
            
            # Sort features by importance
            indices = np.argsort(mean_abs_shap)[::-1]
            
            importance_list = []
            for idx in indices:
                importance_list.append({
                    'feature': self.feature_names[idx],
                    'importance': float(mean_abs_shap[idx])
                })
            
            return importance_list
            
        except Exception as e:
            print(f"Error calculating feature importance: {e}")
            return []


# Global instance
_shap_explainer = None

def get_shap_explainer():
    """Get or create global SHAP explainer instance"""
    global _shap_explainer
    if _shap_explainer is None:
        _shap_explainer = SHAPExplainer()
        _shap_explainer.load_models()
    return _shap_explainer
