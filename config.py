"""
Configuration file for Breast Cancer Detection System
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Model configuration
MODEL_CONFIG = {
    "test_size": 0.2,
    "random_state": 42,
    "n_estimators": 100,
    "max_iter": 1000
}

# Flask configuration
FLASK_CONFIG = {
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 5000
}

# Dataset configuration
DATASET_CONFIG = {
    "target_column": "diagnosis",
    "malignant_label": "M",
    "benign_label": "B"
}
