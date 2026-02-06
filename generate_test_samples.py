"""
Generate sample CSV files for testing the Breast Cancer Detection System
Creates both benign and malignant test cases
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer

def generate_test_samples():
    """Generate sample CSV files for testing"""
    
    # Load the breast cancer dataset
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['diagnosis'] = data.target
    
    # Separate benign and malignant cases
    benign_samples = df[df['diagnosis'] == 1].head(5)
    malignant_samples = df[df['diagnosis'] == 0].head(5)
    
    # Create test samples directory
    import os
    os.makedirs('test_samples', exist_ok=True)
    
    print("=" * 60)
    print("GENERATING TEST SAMPLES")
    print("=" * 60)
    
    # Generate individual benign samples
    for i, (idx, row) in enumerate(benign_samples.iterrows(), 1):
        filename = f'test_samples/benign_sample_{i}.csv'
        sample_df = pd.DataFrame([row[:-1]])  # Exclude diagnosis
        sample_df.to_csv(filename, index=False)
        print(f"✓ Created: {filename}")
        print(f"  Expected: BENIGN")
        print()
    
    # Generate individual malignant samples
    for i, (idx, row) in enumerate(malignant_samples.iterrows(), 1):
        filename = f'test_samples/malignant_sample_{i}.csv'
        sample_df = pd.DataFrame([row[:-1]])  # Exclude diagnosis
        sample_df.to_csv(filename, index=False)
        print(f"✓ Created: {filename}")
        print(f"  Expected: MALIGNANT")
        print()
    
    # Create a combined test file
    combined = pd.concat([benign_samples.head(3), malignant_samples.head(3)])
    combined_df = combined.drop('diagnosis', axis=1)
    combined_df.to_csv('test_samples/mixed_samples.csv', index=False)
    print(f"✓ Created: test_samples/mixed_samples.csv")
    print(f"  Contains: 3 benign + 3 malignant samples")
    print()
    
    # Create a sample with feature values only (no headers for manual input)
    sample_row = benign_samples.iloc[0][:-1]
    with open('test_samples/manual_input_example.txt', 'w') as f:
        f.write("Copy and paste this into the manual input field:\n\n")
        f.write(','.join(map(str, sample_row.values)))
        f.write("\n\nExpected Result: BENIGN")
    print(f"✓ Created: test_samples/manual_input_example.txt")
    print(f"  For manual text input testing")
    print()
    
    # Print feature names for reference
    print("=" * 60)
    print("FEATURE NAMES (30 features):")
    print("=" * 60)
    for i, feature in enumerate(data.feature_names, 1):
        print(f"{i:2d}. {feature}")
    
    print()
    print("=" * 60)
    print("SAMPLE STATISTICS:")
    print("=" * 60)
    print(f"Total samples generated: {len(benign_samples) + len(malignant_samples)}")
    print(f"Benign samples: {len(benign_samples)}")
    print(f"Malignant samples: {len(malignant_samples)}")
    print()
    print("All files saved in 'test_samples/' directory")
    print("=" * 60)
    
    # Display one example
    print()
    print("EXAMPLE - Benign Sample 1 (first 10 features):")
    print("-" * 60)
    example = benign_samples.iloc[0]
    for i, (feature, value) in enumerate(zip(data.feature_names[:10], example[:10])):
        print(f"{feature:30s}: {value:.4f}")
    print("... (20 more features)")
    print()

if __name__ == "__main__":
    generate_test_samples()
    print("\n✅ Test samples generated successfully!")
    print("📁 Check the 'test_samples' folder")
    print("🔬 Upload any CSV file to test the system")
