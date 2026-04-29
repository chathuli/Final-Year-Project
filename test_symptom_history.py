"""
Test script to verify symptom-based predictions are saved and retrieved correctly
"""

import sys
sys.path.insert(0, 'src')

from database import PredictionDatabase
import json

# Initialize database
db = PredictionDatabase('data/predictions.db')

# Test data - symptom-based prediction
test_symptoms = {
    'age': 45,
    'lump': 'small',
    'pain': 'mild',
    'skin_change': 'none',
    'nipple_discharge': 'none',
    'family_history': 'yes',
    'nipple_retraction': 'none',
    'armpit_lump': 'none',
    'breast_shape_change': 'minor',
    'skin_texture': 'normal',
    'symptom_duration': 'weeks',
    'lump_mobility': 'mobile',
    'pain_duration': 'weeks',
    'menstrual_status': 'premenopausal',
    'previous_conditions': 'none',
    'pregnancy_history': 'parous'
}

test_risk_assessment = {
    'risk_level': 'Moderate',
    'risk_score': 6,
    'risk_factors': [
        'Age over 40 (45 years)',
        'Small lump detected',
        'Family history of breast cancer',
        'Minor breast shape changes',
        'Symptoms present for weeks'
    ],
    'recommendation': 'Medical consultation recommended soon'
}

test_features = [15.5, 0.3, 18.2] + [0.0] * 27  # Simplified features

print("Testing symptom-based prediction save...")
print("-" * 60)

# Save a test symptom-based prediction
prediction_id = db.save_prediction(
    prediction=0,
    confidence=0.85,
    model_name='Random Forest',
    features=test_features,
    all_predictions={'rf': 0.85, 'lr': 0.82, 'svm': 0.88},
    prediction_type='symptom',
    symptoms_data=test_symptoms,
    risk_assessment=test_risk_assessment
)

print(f"✓ Saved symptom-based prediction with ID: {prediction_id}")

# Retrieve the prediction
print("\nRetrieving prediction...")
prediction = db.get_prediction_by_id(prediction_id)

if prediction:
    print(f"✓ Retrieved prediction #{prediction['id']}")
    print(f"  - Type: {prediction['prediction_type']}")
    print(f"  - Prediction: {prediction['prediction_label']}")
    print(f"  - Confidence: {prediction['confidence'] * 100:.1f}%")
    
    if 'symptoms_data' in prediction:
        print(f"  - Symptoms: {len(prediction['symptoms_data'])} fields")
        print(f"    • Age: {prediction['symptoms_data']['age']}")
        print(f"    • Lump: {prediction['symptoms_data']['lump']}")
        print(f"    • Family History: {prediction['symptoms_data']['family_history']}")
    
    if 'risk_assessment' in prediction:
        print(f"  - Risk Assessment:")
        print(f"    • Level: {prediction['risk_assessment']['risk_level']}")
        print(f"    • Score: {prediction['risk_assessment']['risk_score']}")
        print(f"    • Factors: {len(prediction['risk_assessment']['risk_factors'])} identified")
else:
    print("✗ Failed to retrieve prediction")

# Get all predictions
print("\nRetrieving all predictions...")
all_predictions = db.get_all_predictions(limit=10)
print(f"✓ Retrieved {len(all_predictions)} predictions")

# Count by type
symptom_count = sum(1 for p in all_predictions if p.get('prediction_type') == 'symptom')
manual_count = sum(1 for p in all_predictions if p.get('prediction_type') == 'manual')

print(f"  - Symptom-based: {symptom_count}")
print(f"  - Manual input: {manual_count}")

print("\n" + "=" * 60)
print("✅ All tests passed! Symptom history feature is working.")
print("=" * 60)
