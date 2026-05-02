"""
Test script for input validation
Tests various invalid inputs to ensure validation works correctly
"""

import sys
sys.path.insert(0, 'src')

from input_validator import InputValidator
import numpy as np

def test_validation():
    """Test input validation with various scenarios"""
    validator = InputValidator()
    
    print("=" * 70)
    print("INPUT VALIDATION TEST SUITE")
    print("=" * 70)
    
    # Test 1: Valid input
    print("\n1. Testing VALID input (30 features, all positive)...")
    valid_features = [15.0, 20.0, 100.0, 700.0, 0.1, 0.15, 0.2, 0.08, 0.18, 0.06,
                      16.0, 22.0, 110.0, 800.0, 0.12, 0.18, 0.25, 0.1, 0.2, 0.07,
                      18.0, 25.0, 120.0, 900.0, 0.14, 0.2, 0.3, 0.12, 0.22, 0.08]
    result = validator.validate_features(valid_features)
    print(f"   Result: {'✓ PASS' if result['valid'] else '✗ FAIL'}")
    if result['warnings']:
        print(f"   Warnings: {len(result['warnings'])}")
    
    # Test 2: Wrong number of features
    print("\n2. Testing INVALID input (only 20 features)...")
    invalid_count = [15.0] * 20
    result = validator.validate_features(invalid_count)
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 3: Negative values
    print("\n3. Testing INVALID input (negative values)...")
    negative_features = valid_features.copy()
    negative_features[0] = -5.0  # Negative radius
    result = validator.validate_features(negative_features)
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 4: NaN values
    print("\n4. Testing INVALID input (NaN values)...")
    nan_features = valid_features.copy()
    nan_features[5] = float('nan')
    result = validator.validate_features(nan_features)
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 5: Infinity values
    print("\n5. Testing INVALID input (Infinity values)...")
    inf_features = valid_features.copy()
    inf_features[10] = float('inf')
    result = validator.validate_features(inf_features)
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 6: Non-numeric values
    print("\n6. Testing INVALID input (string values)...")
    string_features = valid_features.copy()
    string_features[0] = "invalid"
    result = validator.validate_features(string_features)
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 7: Out of range values (warnings)
    print("\n7. Testing input with OUT OF RANGE values (should warn)...")
    extreme_features = valid_features.copy()
    extreme_features[0] = 100.0  # Very large radius
    result = validator.validate_features(extreme_features)
    print(f"   Result: {'✓ PASS' if result['valid'] else '✗ FAIL'}")
    if result['warnings']:
        print(f"   Warnings: {len(result['warnings'])}")
        print(f"   First warning: {result['warnings'][0]}")
    
    # Test 8: Inconsistent mean/worst values
    print("\n8. Testing INCONSISTENT values (mean > worst)...")
    inconsistent_features = valid_features.copy()
    inconsistent_features[0] = 25.0  # radius mean
    inconsistent_features[20] = 15.0  # worst radius (should be >= mean)
    result = validator.validate_features(inconsistent_features)
    print(f"   Result: {'✓ PASS' if result['valid'] else '✗ FAIL'}")
    if result['warnings']:
        print(f"   Warnings: {len(result['warnings'])}")
        for warning in result['warnings']:
            if 'mean' in warning and 'worst' in warning:
                print(f"   Consistency warning: {warning}")
                break
    
    # Test 9: Not a list or array
    print("\n9. Testing INVALID input (not a list/array)...")
    result = validator.validate_features("not a list")
    print(f"   Result: {'✓ PASS (correctly rejected)' if not result['valid'] else '✗ FAIL (should reject)'}")
    if result['errors']:
        print(f"   Error: {result['errors'][0]}")
    
    # Test 10: Numpy array input
    print("\n10. Testing VALID input (numpy array)...")
    numpy_features = np.array(valid_features)
    result = validator.validate_features(numpy_features)
    print(f"   Result: {'✓ PASS' if result['valid'] else '✗ FAIL'}")
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETED")
    print("=" * 70)
    
    # Display feature info
    print("\n" + "=" * 70)
    print("FEATURE INFORMATION (First 5 features)")
    print("=" * 70)
    for i in range(5):
        info = validator.get_feature_info(i)
        print(f"\nFeature {i}:")
        print(f"  Name: {info['name']}")
        print(f"  Expected range: {info['expected_range']}")

if __name__ == '__main__':
    test_validation()
