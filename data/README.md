# Dataset Directory

## About the Dataset

This project uses the **Wisconsin Breast Cancer Dataset** for training and testing the machine learning models.

### Dataset Information

- **Source**: UCI Machine Learning Repository / Kaggle
- **Features**: 30 numeric features computed from digitized images of breast mass
- **Target**: Diagnosis (M = Malignant, B = Benign)
- **Samples**: 569 instances

### Features Include:

1. Radius (mean of distances from center to points on the perimeter)
2. Texture (standard deviation of gray-scale values)
3. Perimeter
4. Area
5. Smoothness (local variation in radius lengths)
6. Compactness (perimeter^2 / area - 1.0)
7. Concavity (severity of concave portions of the contour)
8. Concave points (number of concave portions of the contour)
9. Symmetry
10. Fractal dimension

Each feature has three measurements: mean, standard error, and worst (largest).

### How to Get the Dataset

1. **Option 1**: Download from Kaggle
   - Visit: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
   - Download and place data.csv in this directory

2. **Option 2**: Use scikit-learn
   `python
   from sklearn.datasets import load_breast_cancer
   import pandas as pd
   
   data = load_breast_cancer()
   df = pd.DataFrame(data.data, columns=data.feature_names)
   df['diagnosis'] = data.target
   df.to_csv('data/breast_cancer.csv', index=False)
   `

### File Format

The CSV file should have:
- First row: Column headers
- Subsequent rows: Data samples
- Last column: Target variable (diagnosis)

### Data Privacy

- Ensure all data is anonymized
- Do not share patient information
- Follow HIPAA and data protection guidelines

