"""
Utility functions for Breast Cancer Detection System
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc

def plot_confusion_matrix(y_true, y_pred, save_path=None):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=["Benign", "Malignant"],
                yticklabels=["Benign", "Malignant"])
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_roc_curve(y_true, y_pred_proba, save_path=None):
    """Plot ROC curve"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="darkorange", lw=2, 
             label=f"ROC curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend(loc="lower right")
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_feature_importance(model, feature_names, top_n=10, save_path=None):
    """Plot feature importance for tree-based models"""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(10, 6))
        plt.title(f"Top {top_n} Feature Importances")
        plt.bar(range(top_n), importances[indices])
        plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45, ha="right")
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    else:
        print("Model does not have feature_importances_ attribute")

def validate_input(features, expected_length=30):
    """Validate input features"""
    if not isinstance(features, (list, np.ndarray)):
        raise ValueError("Features must be a list or numpy array")
    
    if len(features) != expected_length:
        raise ValueError(f"Expected {expected_length} features, got {len(features)}")
    
    if not all(isinstance(x, (int, float)) for x in features):
        raise ValueError("All features must be numeric")
    
    return True

def format_prediction_result(prediction, confidence):
    """Format prediction result for display"""
    result = {
        "diagnosis": prediction,
        "confidence": f"{confidence:.2f}%",
        "risk_level": "High" if prediction == "Malignant" and confidence > 80 else "Medium" if confidence > 60 else "Low",
        "recommendation": get_recommendation(prediction, confidence)
    }
    return result

def get_recommendation(prediction, confidence):
    """Get medical recommendation based on prediction"""
    if prediction == "Malignant":
        if confidence > 80:
            return "Immediate consultation with oncologist recommended"
        else:
            return "Further diagnostic tests recommended"
    else:
        if confidence > 80:
            return "Regular monitoring recommended"
        else:
            return "Additional screening may be beneficial"

