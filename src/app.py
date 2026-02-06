"""
Flask Web Application for Breast Cancer Detection
Enhanced with Multi-Model Comparison, History, and Reports
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import os
from datetime import datetime
from enhanced_predict import EnhancedPredictor
from database import PredictionDatabase
from report_generator import ReportGenerator

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize components
predictor = EnhancedPredictor()
db = PredictionDatabase()
report_gen = ReportGenerator()

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests with enhanced features"""
    try:
        # Get data from request
        data = request.get_json()
        features = data.get('features', [])
        
        if not features:
            return jsonify({'error': 'No features provided'}), 400
        
        # Make prediction with all models
        result = predictor.predict_all_models(features)
        
        # Get feature importance
        feature_importance = predictor.get_feature_importance(features)
        result['feature_importance'] = feature_importance
        
        # Get risk assessment
        risk = predictor.get_risk_assessment(
            result['best_model']['prediction'],
            result['best_model']['confidence']
        )
        result['risk_assessment'] = risk
        
        # Save to database
        prediction_id = db.save_prediction(
            prediction=result['best_model']['prediction'],
            confidence=result['best_model']['confidence'],
            model_name=result['best_model']['name'],
            features=features,
            all_predictions=result['all_models']
        )
        
        result['prediction_id'] = prediction_id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """Prediction history page"""
    return render_template('history.html')

@app.route('/api/history')
def get_history():
    """Get prediction history"""
    try:
        predictions = db.get_all_predictions(limit=100)
        return jsonify({'predictions': predictions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get prediction statistics"""
    try:
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/generate-report/<int:prediction_id>')
def generate_report(prediction_id):
    """Generate PDF report for a prediction"""
    try:
        # Get prediction data
        prediction_data = db.get_prediction_by_id(prediction_id)
        
        if not prediction_data:
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Format data for report generator
        formatted_data = {
            'report_id': f"BCR-{prediction_id:06d}",
            'best_model': {
                'name': prediction_data['model_name'],
                'prediction': prediction_data['prediction'],
                'prediction_label': prediction_data['prediction_label'],
                'confidence': prediction_data['confidence']
            },
            'all_models': prediction_data.get('all_model_predictions', {}),
            'feature_importance': [],  # Can be regenerated if needed
            'risk_assessment': {
                'level': 'Medium',
                'message': 'Consult with healthcare professional for detailed assessment'
            }
        }
        
        # Generate report with absolute path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"breast_cancer_report_{prediction_id}_{timestamp}.pdf"
        
        # Use absolute path from project root
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(project_root, 'reports')
        
        # Create reports directory if it doesn't exist
        os.makedirs(reports_dir, exist_ok=True)
        
        output_path = os.path.join(reports_dir, filename)
        
        print(f"Generating report at: {output_path}")
        
        report_path = report_gen.generate_report(formatted_data, output_path)
        
        print(f"Report generated successfully: {report_path}")
        
        # Send file
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Load models on startup
    predictor.load_models()
    
    # Run app
    print("=" * 50)
    print("🚀 Breast Cancer Detection System")
    print("=" * 50)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Use Waitress for production-ready server (no warning)
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except ImportError:
        # Fallback to Flask dev server if Waitress not installed
        app.run(debug=True, host='0.0.0.0', port=5000)
