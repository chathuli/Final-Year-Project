"""
Symptom to Feature Mapper
Converts user-friendly symptoms to Wisconsin dataset features
"""

import numpy as np

class SymptomMapper:
    """
    Maps clinical symptoms to Wisconsin Breast Cancer dataset features.
    This allows users to input symptoms instead of technical measurements.
    """
    
    def __init__(self):
        # Medical research-based weights for symptom importance
        self.symptom_weights = {
            'age': {'young': 0.3, 'middle': 0.6, 'senior': 0.9},
            'lump': {'none': 0.1, 'small': 0.5, 'large': 0.9},
            'pain': {'none': 0.1, 'mild': 0.3, 'severe': 0.6},
            'skin_change': {'none': 0.1, 'dimpling': 0.7, 'redness': 0.8},
            'nipple_discharge': {'none': 0.1, 'clear': 0.4, 'bloody': 0.9},
            'family_history': {'no': 0.2, 'yes': 0.8}
        }
    
    def map_symptoms_to_features(self, symptoms):
        """
        Convert symptoms to 30 Wisconsin dataset features
        
        Args:
            symptoms (dict): User symptoms
                - age: int (patient age)
                - lump: str ('none', 'small', 'large')
                - pain: str ('none', 'mild', 'severe')
                - skin_change: str ('none', 'dimpling', 'redness')
                - nipple_discharge: str ('none', 'clear', 'bloody')
                - family_history: str ('no', 'yes')
        
        Returns:
            list: 30 features matching Wisconsin dataset format
        """
        features = np.zeros(30)
        
        # Age factor (affects multiple features)
        age = symptoms.get('age', 30)
        age_factor = self._get_age_factor(age)
        
        # Lump characteristics (most important indicator)
        lump = symptoms.get('lump', 'none')
        lump_weight = self.symptom_weights['lump'].get(lump, 0.1)
        
        # Pain level
        pain = symptoms.get('pain', 'none')
        pain_weight = self.symptom_weights['pain'].get(pain, 0.1)
        
        # Skin changes
        skin_change = symptoms.get('skin_change', 'none')
        skin_weight = self.symptom_weights['skin_change'].get(skin_change, 0.1)
        
        # Nipple discharge
        nipple_discharge = symptoms.get('nipple_discharge', 'none')
        nipple_weight = self.symptom_weights['nipple_discharge'].get(nipple_discharge, 0.1)
        
        # Family history
        family_history = symptoms.get('family_history', 'no')
        family_weight = self.symptom_weights['family_history'].get(family_history, 0.2)
        
        # Map to Wisconsin features (mean values: 0-9)
        # Radius features (0-2)
        features[0] = 10 + (lump_weight * 10) + (age_factor * 5)  # radius_mean
        features[1] = 0.2 + (lump_weight * 0.5)  # radius_se
        features[2] = 12 + (lump_weight * 15)  # radius_worst
        
        # Texture features (3-5)
        features[3] = 15 + (skin_weight * 10) + (lump_weight * 5)  # texture_mean
        features[4] = 0.8 + (skin_weight * 0.5)  # texture_se
        features[5] = 18 + (skin_weight * 12)  # texture_worst
        
        # Perimeter features (6-8)
        features[6] = 70 + (lump_weight * 50) + (age_factor * 20)  # perimeter_mean
        features[7] = 1.5 + (lump_weight * 2)  # perimeter_se
        features[8] = 80 + (lump_weight * 70)  # perimeter_worst
        
        # Area features (9-11)
        features[9] = 400 + (lump_weight * 600) + (age_factor * 200)  # area_mean
        features[10] = 20 + (lump_weight * 40)  # area_se
        features[11] = 500 + (lump_weight * 800)  # area_worst
        
        # Smoothness features (12-14)
        features[12] = 0.08 + (skin_weight * 0.05) + (lump_weight * 0.03)  # smoothness_mean
        features[13] = 0.005 + (skin_weight * 0.003)  # smoothness_se
        features[14] = 0.10 + (skin_weight * 0.06)  # smoothness_worst
        
        # Compactness features (15-17)
        features[15] = 0.05 + (lump_weight * 0.15) + (skin_weight * 0.08)  # compactness_mean
        features[16] = 0.01 + (lump_weight * 0.02)  # compactness_se
        features[17] = 0.08 + (lump_weight * 0.20)  # compactness_worst
        
        # Concavity features (18-20)
        features[18] = 0.03 + (lump_weight * 0.20) + (skin_weight * 0.10)  # concavity_mean
        features[19] = 0.01 + (lump_weight * 0.03)  # concavity_se
        features[20] = 0.05 + (lump_weight * 0.30)  # concavity_worst
        
        # Concave points features (21-23)
        features[21] = 0.02 + (lump_weight * 0.08) + (nipple_weight * 0.05)  # concave_points_mean
        features[22] = 0.005 + (lump_weight * 0.01)  # concave_points_se
        features[23] = 0.03 + (lump_weight * 0.12)  # concave_points_worst
        
        # Symmetry features (24-26)
        features[24] = 0.15 + (skin_weight * 0.05) + (lump_weight * 0.03)  # symmetry_mean
        features[25] = 0.01 + (skin_weight * 0.01)  # symmetry_se
        features[26] = 0.20 + (skin_weight * 0.08)  # symmetry_worst
        
        # Fractal dimension features (27-29)
        features[27] = 0.055 + (lump_weight * 0.015) + (age_factor * 0.01)  # fractal_dimension_mean
        features[28] = 0.002 + (lump_weight * 0.003)  # fractal_dimension_se
        features[29] = 0.065 + (lump_weight * 0.020)  # fractal_dimension_worst
        
        # Apply pain factor (reduces confidence slightly)
        if pain_weight > 0.3:
            features = features * 0.95
        
        # Apply family history factor (increases risk)
        if family_weight > 0.5:
            features = features * 1.1
        
        return features.tolist()
    
    def _get_age_factor(self, age):
        """Calculate age risk factor"""
        if age < 30:
            return 0.3
        elif age < 40:
            return 0.5
        elif age < 50:
            return 0.7
        elif age < 60:
            return 0.85
        else:
            return 1.0
    
    def get_risk_assessment(self, symptoms):
        """
        Provide a preliminary risk assessment based on symptoms
        
        Returns:
            dict: Risk level and explanation
        """
        risk_score = 0
        risk_factors = []
        
        # Age risk
        age = symptoms.get('age', 30)
        if age > 50:
            risk_score += 2
            risk_factors.append(f"Age over 50 ({age} years)")
        elif age > 40:
            risk_score += 1
            risk_factors.append(f"Age over 40 ({age} years)")
        
        # Lump risk
        lump = symptoms.get('lump', 'none')
        if lump == 'large':
            risk_score += 3
            risk_factors.append("Large lump detected")
        elif lump == 'small':
            risk_score += 2
            risk_factors.append("Small lump detected")
        
        # Skin changes risk
        skin_change = symptoms.get('skin_change', 'none')
        if skin_change in ['dimpling', 'redness']:
            risk_score += 2
            risk_factors.append(f"Skin changes: {skin_change}")
        
        # Nipple discharge risk
        nipple_discharge = symptoms.get('nipple_discharge', 'none')
        if nipple_discharge == 'bloody':
            risk_score += 3
            risk_factors.append("Bloody nipple discharge")
        elif nipple_discharge == 'clear':
            risk_score += 1
            risk_factors.append("Clear nipple discharge")
        
        # Family history risk
        family_history = symptoms.get('family_history', 'no')
        if family_history == 'yes':
            risk_score += 2
            risk_factors.append("Family history of breast cancer")
        
        # Pain (less significant)
        pain = symptoms.get('pain', 'none')
        if pain == 'severe':
            risk_score += 1
            risk_factors.append("Severe pain")
        
        # Determine risk level
        if risk_score >= 8:
            risk_level = "High"
            recommendation = "Immediate medical consultation strongly recommended"
        elif risk_score >= 5:
            risk_level = "Moderate"
            recommendation = "Medical consultation recommended soon"
        elif risk_score >= 2:
            risk_level = "Low-Moderate"
            recommendation = "Consider scheduling a check-up"
        else:
            risk_level = "Low"
            recommendation = "Continue regular self-examinations"
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendation': recommendation
        }
