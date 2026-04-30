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

# Email configuration (Gmail SMTP)
# SECURITY: Set these as environment variables
#   EMAIL_USER     — your Gmail address  e.g. yourname@gmail.com
#   EMAIL_PASSWORD — Gmail App Password  (not your normal password)
#                    Generate at: https://myaccount.google.com/apppasswords
EMAIL_CONFIG = {
    "EMAIL_HOST":     "smtp.gmail.com",
    "EMAIL_PORT":     587,
    "EMAIL_USER":     os.environ.get("EMAIL_USER", ""),
    "EMAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD", ""),
}

# Dataset configuration
DATASET_CONFIG = {
    "target_column": "diagnosis",
    "malignant_label": "M",
    "benign_label": "B"
}
