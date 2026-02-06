"""
Setup script for Breast Cancer Detection System
"""

from setuptools import setup, find_packages

setup(
    name="breast-cancer-detection",
    version="1.0.0",
    description="AI-Based Breast Cancer Detection System using Machine Learning",
    author="Student ID: 10953361",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
        "tensorflow>=2.15.0",
        "keras>=2.15.0",
        "joblib>=1.3.2",
        "pillow>=10.0.0",
        "werkzeug>=3.0.1"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
