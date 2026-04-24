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
            'family_history': {'no': 0.2, 'yes': 0.8},
            # New professional symptoms
            'nipple_retraction': {'none': 0.1, 'recent': 0.7, 'longstanding': 0.5},
            'armpit_lump': {'none': 0.1, 'small': 0.7, 'large': 0.9},
            'breast_shape_change': {'none': 0.1, 'minor': 0.5, 'significant': 0.8},
            'skin_texture': {'normal': 0.1, 'thickened': 0.6, 'orange_peel': 0.9},
            'symptom_duration': {'days': 0.3, 'weeks': 0.5, 'months': 0.7, 'years': 0.4},
            'lump_mobility': {'mobile': 0.3, 'somewhat_fixed': 0.6, 'fixed': 0.9},
            'pain_duration': {'none': 0.1, 'days': 0.2, 'weeks': 0.4, 'months': 0.5},
            'menstrual_status': {'premenopausal': 0.3, 'perimenopausal': 0.5, 'postmenopausal': 0.7},
            'previous_conditions': {'none': 0.2, 'benign_lumps': 0.4, 'biopsy': 0.6, 'surgery': 0.5},
            'pregnancy_history': {'nulliparous': 0.5, 'parous': 0.3, 'currently_pregnant': 0.2, 'breastfeeding': 0.2}
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
                - nipple_retraction: str ('none', 'recent', 'longstanding')
                - armpit_lump: str ('none', 'small', 'large')
                - breast_shape_change: str ('none', 'minor', 'significant')
                - skin_texture: str ('normal', 'thickened', 'orange_peel')
                - symptom_duration: str ('days', 'weeks', 'months', 'years')
                - lump_mobility: str ('mobile', 'somewhat_fixed', 'fixed')
                - pain_duration: str ('none', 'days', 'weeks', 'months')
                - menstrual_status: str ('premenopausal', 'perimenopausal', 'postmenopausal')
                - previous_conditions: str ('none', 'benign_lumps', 'biopsy', 'surgery')
                - pregnancy_history: str ('nulliparous', 'parous', 'currently_pregnant', 'breastfeeding')
        
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
        
        # New professional symptoms
        nipple_retraction = symptoms.get('nipple_retraction', 'none')
        nipple_retraction_weight = self.symptom_weights['nipple_retraction'].get(nipple_retraction, 0.1)
        
        armpit_lump = symptoms.get('armpit_lump', 'none')
        armpit_weight = self.symptom_weights['armpit_lump'].get(armpit_lump, 0.1)
        
        breast_shape_change = symptoms.get('breast_shape_change', 'none')
        shape_weight = self.symptom_weights['breast_shape_change'].get(breast_shape_change, 0.1)
        
        skin_texture = symptoms.get('skin_texture', 'normal')
        texture_weight = self.symptom_weights['skin_texture'].get(skin_texture, 0.1)
        
        symptom_duration = symptoms.get('symptom_duration', 'days')
        duration_weight = self.symptom_weights['symptom_duration'].get(symptom_duration, 0.3)
        
        lump_mobility = symptoms.get('lump_mobility', 'mobile')
        # If no lump detected, lump mobility should be irrelevant (use lowest risk value)
        if lump == 'none':
            lump_mobility = 'mobile'
        mobility_weight = self.symptom_weights['lump_mobility'].get(lump_mobility, 0.3)
        
        pain_duration = symptoms.get('pain_duration', 'none')
        # If no pain, pain duration should be 'none'
        if pain == 'none':
            pain_duration = 'none'
        pain_duration_weight = self.symptom_weights['pain_duration'].get(pain_duration, 0.1)
        
        menstrual_status = symptoms.get('menstrual_status', 'premenopausal')
        menstrual_weight = self.symptom_weights['menstrual_status'].get(menstrual_status, 0.3)
        
        previous_conditions = symptoms.get('previous_conditions', 'none')
        previous_weight = self.symptom_weights['previous_conditions'].get(previous_conditions, 0.2)
        
        pregnancy_history = symptoms.get('pregnancy_history', 'parous')
        pregnancy_weight = self.symptom_weights['pregnancy_history'].get(pregnancy_history, 0.3)
        
        # Calculate overall symptom severity to determine if truly asymptomatic
        overall_severity = (lump_weight + pain_weight + skin_weight + nipple_weight + 
                          nipple_retraction_weight + armpit_weight + shape_weight + 
                          texture_weight + mobility_weight) / 9
        
        # If truly asymptomatic (all weights near baseline 0.1), use healthy baseline values
        if overall_severity < 0.15:  # All symptoms are "none"
            # Use typical benign/healthy tissue values
            features[0] = 11.0  # radius_mean - small, healthy
            features[1] = 0.3   # radius_se
            features[2] = 12.0  # radius_worst
        else:
            # Map to Wisconsin features (mean values: 0-9)
            # Radius features (0-2) - Enhanced with mobility and armpit involvement
            features[0] = 10 + (lump_weight * 10) + (age_factor * 5) + (mobility_weight * 3) + (armpit_weight * 2)  # radius_mean
            features[1] = 0.2 + (lump_weight * 0.5) + (mobility_weight * 0.2)  # radius_se
            features[2] = 12 + (lump_weight * 15) + (mobility_weight * 5) + (armpit_weight * 3)  # radius_worst
        
        if overall_severity < 0.15:  # All symptoms are "none" - use healthy baseline
            # Texture features - healthy tissue
            features[3] = 16.0  # texture_mean
            features[4] = 0.9   # texture_se
            features[5] = 18.0  # texture_worst
            
            # Perimeter features - healthy
            features[6] = 72.0  # perimeter_mean
            features[7] = 1.8   # perimeter_se
            features[8] = 80.0  # perimeter_worst
            
            # Area features - healthy
            features[9] = 420.0  # area_mean
            features[10] = 25.0  # area_se
            features[11] = 500.0 # area_worst
            
            # Smoothness features - healthy
            features[12] = 0.09  # smoothness_mean
            features[13] = 0.006 # smoothness_se
            features[14] = 0.11  # smoothness_worst
            
            # Compactness features - healthy
            features[15] = 0.06  # compactness_mean
            features[16] = 0.015 # compactness_se
            features[17] = 0.10  # compactness_worst
            
            # Concavity features - healthy
            features[18] = 0.04  # concavity_mean
            features[19] = 0.012 # concavity_se
            features[20] = 0.07  # concavity_worst
            
            # Concave points features - healthy
            features[21] = 0.025 # concave_points_mean
            features[22] = 0.007 # concave_points_se
            features[23] = 0.04  # concave_points_worst
            
            # Symmetry features - healthy
            features[24] = 0.16  # symmetry_mean
            features[25] = 0.015 # symmetry_se
            features[26] = 0.21  # symmetry_worst
            
            # Fractal dimension features - healthy
            features[27] = 0.058 # fractal_dimension_mean
            features[28] = 0.003 # fractal_dimension_se
            features[29] = 0.070 # fractal_dimension_worst
        else:
            # Texture features (3-5) - Enhanced with skin texture and shape changes
            features[3] = 15 + (skin_weight * 10) + (lump_weight * 5) + (texture_weight * 8) + (shape_weight * 4)  # texture_mean
            features[4] = 0.8 + (skin_weight * 0.5) + (texture_weight * 0.4)  # texture_se
            features[5] = 18 + (skin_weight * 12) + (texture_weight * 10) + (shape_weight * 5)  # texture_worst
            
            # Perimeter features (6-8) - Enhanced with duration and shape
            features[6] = 70 + (lump_weight * 50) + (age_factor * 20) + (duration_weight * 15) + (shape_weight * 10)  # perimeter_mean
            features[7] = 1.5 + (lump_weight * 2) + (duration_weight * 0.8)  # perimeter_se
            features[8] = 80 + (lump_weight * 70) + (duration_weight * 20) + (shape_weight * 15)  # perimeter_worst
            
            # Area features (9-11) - Enhanced with mobility and armpit
            features[9] = 400 + (lump_weight * 600) + (age_factor * 200) + (mobility_weight * 150) + (armpit_weight * 100)  # area_mean
            features[10] = 20 + (lump_weight * 40) + (mobility_weight * 15)  # area_se
            features[11] = 500 + (lump_weight * 800) + (mobility_weight * 200) + (armpit_weight * 150)  # area_worst
            
            # Smoothness features (12-14) - Enhanced with skin texture
            features[12] = 0.08 + (skin_weight * 0.05) + (lump_weight * 0.03) + (texture_weight * 0.04)  # smoothness_mean
            features[13] = 0.005 + (skin_weight * 0.003) + (texture_weight * 0.002)  # smoothness_se
            features[14] = 0.10 + (skin_weight * 0.06) + (texture_weight * 0.05)  # smoothness_worst
            
            # Compactness features (15-17) - Enhanced with mobility and texture
            features[15] = 0.05 + (lump_weight * 0.15) + (skin_weight * 0.08) + (mobility_weight * 0.10) + (texture_weight * 0.08)  # compactness_mean
            features[16] = 0.01 + (lump_weight * 0.02) + (mobility_weight * 0.015)  # compactness_se
            features[17] = 0.08 + (lump_weight * 0.20) + (mobility_weight * 0.15) + (texture_weight * 0.12)  # compactness_worst
            
            # Concavity features (18-20) - Enhanced with nipple retraction and shape
            features[18] = 0.03 + (lump_weight * 0.20) + (skin_weight * 0.10) + (nipple_retraction_weight * 0.15) + (shape_weight * 0.12)  # concavity_mean
            features[19] = 0.01 + (lump_weight * 0.03) + (nipple_retraction_weight * 0.02)  # concavity_se
            features[20] = 0.05 + (lump_weight * 0.30) + (nipple_retraction_weight * 0.20) + (shape_weight * 0.15)  # concavity_worst
            
            # Concave points features (21-23) - Enhanced with nipple changes
            features[21] = 0.02 + (lump_weight * 0.08) + (nipple_weight * 0.05) + (nipple_retraction_weight * 0.06)  # concave_points_mean
            features[22] = 0.005 + (lump_weight * 0.01) + (nipple_retraction_weight * 0.008)  # concave_points_se
            features[23] = 0.03 + (lump_weight * 0.12) + (nipple_retraction_weight * 0.10)  # concave_points_worst
            
            # Symmetry features (24-26) - Enhanced with shape changes
            features[24] = 0.15 + (skin_weight * 0.05) + (lump_weight * 0.03) + (shape_weight * 0.06) + (nipple_retraction_weight * 0.04)  # symmetry_mean
            features[25] = 0.01 + (skin_weight * 0.01) + (shape_weight * 0.008)  # symmetry_se
            features[26] = 0.20 + (skin_weight * 0.08) + (shape_weight * 0.10)  # symmetry_worst
            
            # Fractal dimension features (27-29) - Enhanced with menstrual and previous conditions
            features[27] = 0.055 + (lump_weight * 0.015) + (age_factor * 0.01) + (menstrual_weight * 0.008) + (previous_weight * 0.006)  # fractal_dimension_mean
            features[28] = 0.002 + (lump_weight * 0.003) + (menstrual_weight * 0.002)  # fractal_dimension_se
            features[29] = 0.065 + (lump_weight * 0.020) + (menstrual_weight * 0.012) + (previous_weight * 0.010)  # fractal_dimension_worst
        
        # Only apply modifiers if there are actual symptoms
        if overall_severity >= 0.15:
            # Apply pain factor (reduces confidence slightly)
            if pain_weight > 0.3:
                features = features * 0.95
            
            # Apply family history factor (increases risk)
            if family_weight > 0.5:
                features = features * 1.1
            
            # Apply pregnancy/breastfeeding factor (may reduce risk)
            if pregnancy_weight < 0.3:
                features = features * 1.05
            
            # Apply duration factor (longer duration may indicate chronic benign condition)
            if duration_weight > 0.6:
                features = features * 1.08
        
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
        
        # NEW PROFESSIONAL SYMPTOMS
        
        # Nipple retraction (HIGH RISK)
        nipple_retraction = symptoms.get('nipple_retraction', 'none')
        if nipple_retraction == 'recent':
            risk_score += 3
            risk_factors.append("Recent nipple retraction/inversion")
        elif nipple_retraction == 'longstanding':
            risk_score += 1
            risk_factors.append("Longstanding nipple retraction")
        
        # Armpit lump (HIGH RISK - lymph node involvement)
        armpit_lump = symptoms.get('armpit_lump', 'none')
        if armpit_lump == 'large':
            risk_score += 3
            risk_factors.append("Large armpit lump (possible lymph node)")
        elif armpit_lump == 'small':
            risk_score += 2
            risk_factors.append("Small armpit lump detected")
        
        # Breast shape changes
        breast_shape_change = symptoms.get('breast_shape_change', 'none')
        if breast_shape_change == 'significant':
            risk_score += 2
            risk_factors.append("Significant breast shape changes")
        elif breast_shape_change == 'minor':
            risk_score += 1
            risk_factors.append("Minor breast shape changes")
        
        # Skin texture (Peau d'Orange is HIGH RISK)
        skin_texture = symptoms.get('skin_texture', 'normal')
        if skin_texture == 'orange_peel':
            risk_score += 3
            risk_factors.append("Orange peel skin texture (peau d'orange)")
        elif skin_texture == 'thickened':
            risk_score += 2
            risk_factors.append("Thickened breast skin")
        
        # Symptom duration
        symptom_duration = symptoms.get('symptom_duration', 'days')
        if symptom_duration in ['months', 'years']:
            risk_score += 1
            risk_factors.append(f"Symptoms present for {symptom_duration}")
        
        # Lump mobility (fixed lumps are concerning)
        lump_mobility = symptoms.get('lump_mobility', 'mobile')
        if lump_mobility == 'fixed' and lump != 'none':
            risk_score += 3
            risk_factors.append("Fixed/immobile lump")
        elif lump_mobility == 'somewhat_fixed' and lump != 'none':
            risk_score += 2
            risk_factors.append("Partially fixed lump")
        
        # Pain duration
        pain_duration = symptoms.get('pain_duration', 'none')
        if pain_duration in ['weeks', 'months']:
            risk_score += 1
            risk_factors.append(f"Pain lasting {pain_duration}")
        
        # Menstrual status
        menstrual_status = symptoms.get('menstrual_status', 'premenopausal')
        if menstrual_status == 'postmenopausal':
            risk_score += 1
            risk_factors.append("Postmenopausal status")
        
        # Previous breast conditions
        previous_conditions = symptoms.get('previous_conditions', 'none')
        if previous_conditions == 'biopsy':
            risk_score += 2
            risk_factors.append("Previous breast biopsy")
        elif previous_conditions in ['benign_lumps', 'surgery']:
            risk_score += 1
            risk_factors.append(f"Previous breast condition: {previous_conditions}")
        
        # Pregnancy/breastfeeding history
        pregnancy_history = symptoms.get('pregnancy_history', 'parous')
        if pregnancy_history == 'nulliparous':
            risk_score += 1
            risk_factors.append("No pregnancy history (nulliparous)")
        
        # Determine risk level (adjusted for new symptoms)
        if risk_score >= 12:
            risk_level = "Very High"
            recommendation = "URGENT: Seek immediate medical attention"
        elif risk_score >= 8:
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
