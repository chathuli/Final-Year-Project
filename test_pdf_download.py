"""
Quick test script to verify PDF generation works
"""

import os
import sys

# Add src to path
sys.path.insert(0, 'src')

from report_generator import ReportGenerator
from datetime import datetime

# Test data
test_data = {
    'report_id': 'BCR-000001',
    'best_model': {
        'name': 'Logistic Regression',
        'prediction': 0,
        'prediction_label': 'Benign',
        'confidence': 0.982
    },
    'all_models': {
        'Logistic Regression': {
            'prediction_label': 'Benign',
            'confidence': 0.982
        },
        'Random Forest': {
            'prediction_label': 'Benign',
            'confidence': 0.956
        },
        'SVM': {
            'prediction_label': 'Benign',
            'confidence': 0.982
        }
    },
    'feature_importance': [],
    'risk_assessment': {
        'level': 'Low',
        'message': 'High confidence benign prediction'
    }
}

# Generate report
report_gen = ReportGenerator()

# Use absolute path
project_root = os.path.dirname(os.path.abspath(__file__))
reports_dir = os.path.join(project_root, 'reports')
os.makedirs(reports_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"test_report_{timestamp}.pdf"
output_path = os.path.join(reports_dir, filename)

print(f"Generating test report at: {output_path}")

try:
    report_path = report_gen.generate_report(test_data, output_path)
    print(f"✅ Report generated successfully!")
    print(f"📄 Location: {report_path}")
    print(f"📁 File exists: {os.path.exists(report_path)}")
    print(f"📊 File size: {os.path.getsize(report_path)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
