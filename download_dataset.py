"""
Download Wisconsin Breast Cancer Dataset using scikit-learn
"""

from sklearn.datasets import load_breast_cancer
import pandas as pd
import os

def download_dataset():
    """Download and save the breast cancer dataset"""
    print("Downloading Wisconsin Breast Cancer Dataset...")
    
    # Load dataset from scikit-learn
    data = load_breast_cancer()
    
    # Create DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['diagnosis'] = data.target
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    filepath = 'data/breast_cancer.csv'
    df.to_csv(filepath, index=False)
    
    print(f"Dataset downloaded successfully!")
    print(f"Saved to: {filepath}")
    print(f"Shape: {df.shape}")
    print(f"Features: {len(data.feature_names)}")
    print(f"Samples: {len(df)}")
    print(f"\nTarget distribution:")
    print(f"  Benign (1): {sum(data.target == 1)}")
    print(f"  Malignant (0): {sum(data.target == 0)}")

if __name__ == "__main__":
    download_dataset()
