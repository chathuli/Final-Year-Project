"""
Input Validation Module for Breast Cancer Prediction
Validates feature inputs to ensure data quality and prevent errors
"""

import numpy as np
from sklearn.datasets import load_breast_cancer

class InputValidator:
    """Validates input features for breast cancer prediction"""
    
    def __init__(self):
        """Initialize validator with feature names and reasonable bounds"""
        self.feature_names = load_breast_cancer().feature_names.tolist()
        
        # Define reasonable bounds for each feature based on Wisconsin dataset
        # These are approximate ranges from the dataset
        self.feature_bounds = {
            # Radius features (in mm)
            'radius': (0, 50),
            # Texture features (standard deviation of gray-scale values)
            'texture': (0, 50),
            # Perimeter features (in mm)
            'perimeter': (0, 300),
            # Area features (in mm²)
            'area': (0, 3000),
            # Smoothness features (local variation in radius lengths)
            'smoothness': (0, 0.3),
            # Compactness features (perimeter² / area - 1.0)
            'compactness': (0, 0.5),
            # Concavity features (severity of concave portions)
            'concavity': (0, 0.7),
            # Concave points features (number of concave portions)
            'concave points': (0, 0.3),
            # Symmetry features
            'symmetry': (0, 0.5),
            # Fractal dimension features
            'fractal dimension': (0, 0.15)
        }
    
    def validate_features(self, features):
        """
        Validate input features
        
        Args:
            features: List or array of 30 feature values
            
        Returns:
            dict: {
                'valid': bool,
                'errors': list of error messages,
                'warnings': list of warning messages
            }
        """
        errors = []
        warnings = []
        
        # Check 1: Must be a list or array
        if not isinstance(features, (list, np.ndarray)):
            errors.append("Features must be a list or numpy array")
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Convert to list if numpy array
        if isinstance(features, np.ndarray):
            features = features.tolist()
        
        # Check 2: Must have exactly 30 features
        if len(features) != 30:
            errors.append(f"Must provide exactly 30 features, got {len(features)}")
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Check 3: All features must be numeric
        for i, value in enumerate(features):
            if not isinstance(value, (int, float, np.integer, np.floating)):
                errors.append(f"Feature {i} ({self.feature_names[i]}) must be numeric, got {type(value).__name__}")
        
        if errors:
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Check 4: No NaN or Inf values
        for i, value in enumerate(features):
            if np.isnan(value):
                errors.append(f"Feature {i} ({self.feature_names[i]}) is NaN (Not a Number)")
            elif np.isinf(value):
                errors.append(f"Feature {i} ({self.feature_names[i]}) is Inf (Infinity)")
        
        if errors:
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Check 5: All features must be non-negative
        for i, value in enumerate(features):
            if value < 0:
                errors.append(f"Feature {i} ({self.feature_names[i]}) cannot be negative, got {value}")
        
        if errors:
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Check 6: Features should be within reasonable bounds
        for i, value in enumerate(features):
            feature_name = self.feature_names[i]
            
            # Find the appropriate bound for this feature
            bound_key = None
            for key in self.feature_bounds.keys():
                if key in feature_name:
                    bound_key = key
                    break
            
            if bound_key:
                min_val, max_val = self.feature_bounds[bound_key]
                
                if value < min_val:
                    warnings.append(
                        f"Feature {i} ({feature_name}) is unusually low: {value:.4f} "
                        f"(expected >= {min_val})"
                    )
                elif value > max_val:
                    warnings.append(
                        f"Feature {i} ({feature_name}) is unusually high: {value:.4f} "
                        f"(expected <= {max_val})"
                    )
        
        # Check 7: Logical consistency checks
        # Mean should generally be less than worst (max)
        for base_feature in ['radius', 'texture', 'perimeter', 'area', 'smoothness', 
                             'compactness', 'concavity', 'concave points', 'symmetry', 
                             'fractal dimension']:
            try:
                mean_idx = self.feature_names.index(f"{base_feature} mean")
                worst_idx = self.feature_names.index(f"worst {base_feature}")
                
                if features[mean_idx] > features[worst_idx]:
                    warnings.append(
                        f"{base_feature} mean ({features[mean_idx]:.4f}) is greater than "
                        f"worst value ({features[worst_idx]:.4f}) - this is unusual"
                    )
            except ValueError:
                # Feature not found, skip
                pass
        
        # All checks passed
        return {
            'valid': True,
            'errors': [],
            'warnings': warnings
        }
    
    def get_feature_info(self, feature_index):
        """
        Get information about a specific feature
        
        Args:
            feature_index: Index of the feature (0-29)
            
        Returns:
            dict: Feature information including name and expected range
        """
        if feature_index < 0 or feature_index >= 30:
            return {'error': 'Feature index must be between 0 and 29'}
        
        feature_name = self.feature_names[feature_index]
        
        # Find the appropriate bound
        bound_key = None
        for key in self.feature_bounds.keys():
            if key in feature_name:
                bound_key = key
                break
        
        info = {
            'index': feature_index,
            'name': feature_name,
            'expected_range': self.feature_bounds.get(bound_key, (0, float('inf'))) if bound_key else None
        }
        
        return info
    
    def get_all_feature_info(self):
        """Get information about all features"""
        return [self.get_feature_info(i) for i in range(30)]


# Convenience function for quick validation
def validate_input(features):
    """
    Quick validation function
    
    Args:
        features: List or array of 30 feature values
        
    Returns:
        dict: Validation result
    """
    validator = InputValidator()
    return validator.validate_features(features)
