"""
API Testing Script
Demonstrates how to use the Breast Cancer Detection REST API
"""

import requests
import json

# Configuration
API_TOKEN = "YOUR_API_TOKEN_HERE"  # Replace with your actual token
BASE_URL = "http://localhost:5000/api/v1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Sample features (from Wisconsin Breast Cancer Dataset)
# This is a malignant case
malignant_features = [
    17.99, 10.38, 122.8, 1001, 0.1184,
    0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
    1.095, 0.9053, 8.589, 153.4, 0.006399,
    0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
    25.38, 17.33, 184.6, 2019, 0.1622,
    0.6656, 0.7119, 0.2654, 0.4601, 0.1189
]

# This is a benign case
benign_features = [
    13.54, 14.36, 87.46, 566.3, 0.09779,
    0.08129, 0.06664, 0.04781, 0.1885, 0.05766,
    0.2699, 0.7886, 2.058, 23.56, 0.008462,
    0.0146, 0.02387, 0.01315, 0.0198, 0.0023,
    15.11, 19.26, 99.7, 711.2, 0.144,
    0.1773, 0.239, 0.1288, 0.2977, 0.07259
]

def print_separator():
    print("\n" + "="*70 + "\n")

def test_prediction(features, case_name):
    """Test the prediction endpoint"""
    print(f"Testing Prediction - {case_name}")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            headers=headers,
            json={"features": features}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success!")
            print(f"  Prediction ID: {result['prediction_id']}")
            print(f"  Result: {result['prediction_label']}")
            print(f"  Confidence: {result['confidence']:.2f}%")
            print(f"  Model Used: {result['model_used']}")
            print(f"  Risk Level: {result['risk_assessment']['level']}")
            print(f"  Message: {result['risk_assessment']['message']}")
            
            print(f"\n  All Models Agreement:")
            for model_name, model_result in result['all_models'].items():
                print(f"    - {model_name}: {model_result['prediction_label']} ({model_result['confidence']:.2f}%)")
            
            print(f"\n  Top Contributing Features:")
            for i, feat in enumerate(result['feature_importance'][:5], 1):
                print(f"    {i}. {feat['feature']}: {feat['value']:.4f} (importance: {feat['importance']:.4f})")
            
            return result['prediction_id']
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.json()}")
            return None
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return None

def test_history():
    """Test the history endpoint"""
    print("Testing History Endpoint")
    print("-" * 70)
    
    try:
        response = requests.get(
            f"{BASE_URL}/history?limit=5",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success!")
            print(f"  Total Predictions: {result['total']}")
            print(f"  Showing: {len(result['predictions'])} records")
            
            print(f"\n  Recent Predictions:")
            for pred in result['predictions']:
                print(f"    - ID {pred['id']}: {pred['prediction_label']} "
                      f"({pred['confidence']:.2f}%) - {pred['timestamp']}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.json()}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")

def test_statistics():
    """Test the statistics endpoint"""
    print("Testing Statistics Endpoint")
    print("-" * 70)
    
    try:
        response = requests.get(
            f"{BASE_URL}/statistics",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            stats = result['statistics']
            print(f"✓ Success!")
            print(f"  Total Predictions: {stats['total_predictions']}")
            print(f"  Benign Cases: {stats['benign_count']}")
            print(f"  Malignant Cases: {stats['malignant_count']}")
            print(f"  Average Confidence: {stats['average_confidence']:.2f}%")
            
            if 'predictions_last_7_days' in stats:
                print(f"  Last 7 Days: {stats['predictions_last_7_days']} predictions")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.json()}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")

def test_get_prediction(prediction_id):
    """Test getting a specific prediction"""
    print(f"Testing Get Prediction - ID: {prediction_id}")
    print("-" * 70)
    
    try:
        response = requests.get(
            f"{BASE_URL}/prediction/{prediction_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            pred = result['prediction']
            print(f"✓ Success!")
            print(f"  ID: {pred['id']}")
            print(f"  Timestamp: {pred['timestamp']}")
            print(f"  Result: {pred['prediction_label']}")
            print(f"  Confidence: {pred['confidence']:.2f}%")
            print(f"  Model: {pred['model_name']}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.json()}")
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")

def main():
    """Run all API tests"""
    print("\n" + "="*70)
    print("  BREAST CANCER DETECTION API - TEST SUITE")
    print("="*70)
    
    # Check if token is set
    if API_TOKEN == "YOUR_API_TOKEN_HERE":
        print("\n⚠️  WARNING: Please set your API token in the script!")
        print("   1. Log in to http://localhost:5000")
        print("   2. Go to Profile page")
        print("   3. Create an API token")
        print("   4. Replace 'YOUR_API_TOKEN_HERE' with your token")
        print("\n" + "="*70 + "\n")
        return
    
    print_separator()
    
    # Test 1: Malignant prediction
    malignant_id = test_prediction(malignant_features, "Malignant Case")
    print_separator()
    
    # Test 2: Benign prediction
    benign_id = test_prediction(benign_features, "Benign Case")
    print_separator()
    
    # Test 3: Get history
    test_history()
    print_separator()
    
    # Test 4: Get statistics
    test_statistics()
    print_separator()
    
    # Test 5: Get specific prediction
    if malignant_id:
        test_get_prediction(malignant_id)
        print_separator()
    
    print("✓ All tests completed!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
