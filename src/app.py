"""
Flask Web Application for Breast Cancer Detection
Enhanced with Multi-Model Comparison, History, Reports, Authentication, and REST API
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import numpy as np
import os
from datetime import datetime
from enhanced_predict import EnhancedPredictor
from database import PredictionDatabase
from report_generator import ReportGenerator
from auth import AuthManager, login_required, api_token_required, admin_required, doctor_required
from appointments import AppointmentManager

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Initialize components
predictor = EnhancedPredictor()
db = PredictionDatabase()
report_gen = ReportGenerator()
auth_manager = AuthManager()
appointment_manager = AppointmentManager()

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/login')
def login():
    """Login selection page"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login_select.html')

@app.route('/login/admin')
def login_admin():
    """Admin login page"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('admin_login.html')

@app.route('/login/doctor')
def login_doctor():
    """Doctor login page"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('doctor_login.html')

@app.route('/login/user')
def login_user():
    """User login page"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('user_login.html')

@app.route('/register')
def register():
    """Registration page"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    """User profile and API tokens page"""
    user = auth_manager.get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """API endpoint for user registration"""
    data = request.get_json()
    result = auth_manager.register_user(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name')
    )
    return jsonify(result)

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for user login"""
    data = request.get_json()
    result = auth_manager.login_user(
        username=data.get('username'),
        password=data.get('password')
    )
    
    if result['success']:
        session['user_id'] = result['user']['id']
        session['username'] = result['user']['username']
        session['role'] = result['user']['role']
        
        # Redirect based on role
        if result['user']['role'] == 'admin':
            result['redirect'] = '/admin'
        elif result['user']['role'] == 'doctor':
            result['redirect'] = '/doctor'
        else:
            result['redirect'] = '/'
    
    return jsonify(result)

@app.route('/api/auth/tokens', methods=['GET', 'POST'])
@login_required
def api_tokens():
    """Get or create API tokens"""
    if request.method == 'GET':
        tokens = auth_manager.get_user_tokens(session['user_id'])
        return jsonify({'tokens': tokens})
    
    elif request.method == 'POST':
        data = request.get_json()
        result = auth_manager.create_api_token(
            user_id=session['user_id'],
            name=data.get('name'),
            expires_days=data.get('expires_days', 365)
        )
        return jsonify(result)

@app.route('/api/auth/tokens/<int:token_id>', methods=['DELETE'])
@login_required
def api_revoke_token(token_id):
    """Revoke an API token"""
    result = auth_manager.revoke_token(token_id, session['user_id'])
    return jsonify(result)

# ============================================================================
# WEB APPLICATION ROUTES (Protected)
# ============================================================================

@app.route('/')
@login_required
def home():
    """Home page - Symptom Checker (main feature)"""
    return render_template('symptom_input.html')

@app.route('/advanced')
@doctor_required
def advanced():
    """Advanced analysis page - Technical feature input"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
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
        
        # Get feature importance (now uses SHAP if available)
        feature_importance = predictor.get_feature_importance(features)
        result['feature_importance'] = feature_importance
        
        # Get SHAP explanation with visualizations
        try:
            shap_explanation = predictor.get_shap_explanation(features)
            if shap_explanation.get('success'):
                result['shap'] = {
                    'force_plot': shap_explanation.get('force_plot'),
                    'waterfall_plot': shap_explanation.get('waterfall_plot'),
                    'top_features': shap_explanation.get('top_features', [])[:5]
                }
        except Exception as e:
            print(f"SHAP explanation error: {e}")
            # Continue without SHAP if it fails
        
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
@login_required
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
@login_required
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

# ============================================================================
# REST API v1 ENDPOINTS (Token Protected)
# ============================================================================

@app.route('/api/v1/predict', methods=['POST'])
@api_token_required
def api_v1_predict():
    """
    API endpoint for making predictions
    Requires API token authentication
    
    Request Body:
    {
        "features": [array of 30 feature values]
    }
    
    Response:
    {
        "success": true,
        "prediction_id": 123,
        "prediction": 0,
        "prediction_label": "Benign",
        "confidence": 98.5,
        "model_used": "Logistic Regression",
        "all_models": {...},
        "feature_importance": [...],
        "risk_assessment": {...},
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    try:
        data = request.get_json()
        features = data.get('features', [])
        
        if not features:
            return jsonify({
                'success': False,
                'error': 'No features provided',
                'message': 'Please provide an array of 30 feature values'
            }), 400
        
        if len(features) != 30:
            return jsonify({
                'success': False,
                'error': 'Invalid feature count',
                'message': f'Expected 30 features, got {len(features)}'
            }), 400
        
        # Make prediction with all models
        result = predictor.predict_all_models(features)
        
        # Get feature importance
        feature_importance = predictor.get_feature_importance(features)
        
        # Get risk assessment
        risk = predictor.get_risk_assessment(
            result['best_model']['prediction'],
            result['best_model']['confidence']
        )
        
        # Save to database (associate with API user)
        prediction_id = db.save_prediction(
            prediction=result['best_model']['prediction'],
            confidence=result['best_model']['confidence'],
            model_name=result['best_model']['name'],
            features=features,
            all_predictions=result['all_models']
        )
        
        # Format API response
        api_response = {
            'success': True,
            'prediction_id': prediction_id,
            'prediction': result['best_model']['prediction'],
            'prediction_label': result['best_model']['prediction_label'],
            'confidence': result['best_model']['confidence'],
            'model_used': result['best_model']['name'],
            'all_models': result['all_models'],
            'feature_importance': feature_importance,
            'risk_assessment': risk,
            'timestamp': datetime.now().isoformat(),
            'user': request.current_user['username']
        }
        
        return jsonify(api_response), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

@app.route('/api/v1/history', methods=['GET'])
@api_token_required
def api_v1_history():
    """
    Get prediction history
    
    Query Parameters:
    - limit: Number of records to return (default: 100)
    - offset: Number of records to skip (default: 0)
    
    Response:
    {
        "success": true,
        "predictions": [...],
        "total": 150,
        "limit": 100,
        "offset": 0
    }
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        predictions = db.get_all_predictions(limit=limit)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'total': len(predictions),
            'limit': limit,
            'offset': offset,
            'user': request.current_user['username']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve history',
            'message': str(e)
        }), 500

@app.route('/api/v1/statistics', methods=['GET'])
@api_token_required
def api_v1_statistics():
    """
    Get prediction statistics
    
    Response:
    {
        "success": true,
        "statistics": {
            "total_predictions": 150,
            "benign_count": 100,
            "malignant_count": 50,
            "average_confidence": 95.5,
            ...
        }
    }
    """
    try:
        stats = db.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats,
            'user': request.current_user['username']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve statistics',
            'message': str(e)
        }), 500

@app.route('/api/v1/prediction/<int:prediction_id>', methods=['GET'])
@api_token_required
def api_v1_get_prediction(prediction_id):
    """
    Get a specific prediction by ID
    
    Response:
    {
        "success": true,
        "prediction": {...}
    }
    """
    try:
        prediction = db.get_prediction_by_id(prediction_id)
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediction not found',
                'message': f'No prediction found with ID {prediction_id}'
            }), 404
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'user': request.current_user['username']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve prediction',
            'message': str(e)
        }), 500

@app.route('/api/docs')
def api_docs():
    """API Documentation page"""
    return render_template('api_docs.html')

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    print(f"Admin dashboard accessed by user: {session.get('username')}, role: {session.get('role')}")
    return render_template('admin_dashboard.html')

@app.route('/api/admin/statistics')
@admin_required
def admin_statistics():
    """Get admin statistics"""
    try:
        # Get user statistics
        all_users = auth_manager.get_all_users()
        doctors = [u for u in all_users if u['role'] == 'doctor']
        patients = [u for u in all_users if u['role'] == 'user']
        active_users = [u for u in all_users if u['is_active'] == 1]
        inactive_users = [u for u in all_users if u['is_active'] == 0]
        
        # Get prediction statistics
        pred_stats = db.get_statistics()
        
        return jsonify({
            'total_users': len(all_users),
            'total_doctors': len(doctors),
            'total_patients': len(patients),
            'active_users': len(active_users),
            'inactive_users': len(inactive_users),
            'total_predictions': pred_stats.get('total', 0),
            'benign_count': pred_stats.get('benign', 0),
            'malignant_count': pred_stats.get('malignant', 0),
            'avg_confidence': pred_stats.get('avg_confidence', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users')
@admin_required
def admin_get_users():
    """Get all users or filtered by role"""
    try:
        role = request.args.get('role')
        users = auth_manager.get_all_users(role=role)
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/register-doctor', methods=['POST'])
@admin_required
def admin_register_doctor():
    """Register a new doctor"""
    try:
        data = request.get_json()
        result = auth_manager.register_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            full_name=data.get('full_name'),
            role='doctor',
            created_by=session['user_id']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def admin_toggle_user(user_id):
    """Toggle user active status"""
    try:
        result = auth_manager.toggle_user_status(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# DOCTOR ROUTES
# ============================================================================

@app.route('/doctor')
@doctor_required
def doctor_dashboard():
    """Doctor dashboard"""
    return render_template('doctor_dashboard.html')

# ============================================================================
# SYMPTOM-BASED PREDICTION (NEW FEATURE)
# ============================================================================

@app.route('/symptoms')
@login_required
def symptoms():
    """Symptom-based input page (redirects to home)"""
    return redirect(url_for('home'))

@app.route('/predict_symptoms', methods=['POST'])
@login_required
def predict_symptoms():
    """
    Predict based on user symptoms
    Converts symptoms to Wisconsin dataset features
    """
    try:
        from symptom_mapper import SymptomMapper
        
        # Get symptom data
        data = request.get_json()
        
        # Initialize mapper
        mapper = SymptomMapper()
        
        # Convert symptoms to features
        features = mapper.map_symptoms_to_features(data)
        
        # Get risk assessment
        risk_assessment = mapper.get_risk_assessment(data)
        
        # Make prediction with all models
        result = predictor.predict_all_models(features)
        
        # Save to database
        prediction_id = db.save_prediction(
            prediction=result['best_model']['prediction'],
            confidence=result['best_model']['confidence'],
            model_name=result['best_model']['name'],
            features=features,
            all_predictions=result['all_models']
        )
        
        # Format response
        response = {
            'success': True,
            'prediction_id': prediction_id,
            'prediction': result['best_model']['prediction_label'],
            'confidence': result['best_model']['confidence'],
            'model_used': result['best_model']['name'],
            'all_models': result['all_models'],
            'risk_assessment': risk_assessment,
            'symptoms_provided': data,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict_image', methods=['POST'])
@login_required
def predict_image():
    """
    Predict based on uploaded medical image
    Analyzes image and extracts features for prediction
    """
    try:
        from image_analyzer import ImageAnalyzer
        
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No image file selected'
            }), 400
        
        # Initialize analyzer
        analyzer = ImageAnalyzer()
        
        # Analyze image
        analysis_result = analyzer.analyze_image(image_file)
        
        if not analysis_result['success']:
            return jsonify(analysis_result), 400
        
        # Get features from image
        features = analysis_result['features']
        
        # Make prediction with all models
        result = predictor.predict_all_models(features)
        
        # Get risk assessment
        risk = predictor.get_risk_assessment(
            result['best_model']['prediction'],
            result['best_model']['confidence']
        )
        
        # Save to database
        prediction_id = db.save_prediction(
            prediction=result['best_model']['prediction'],
            confidence=result['best_model']['confidence'],
            model_name=result['best_model']['name'],
            features=features,
            all_predictions=result['all_models']
        )
        
        # Format response
        response = {
            'success': True,
            'prediction_id': prediction_id,
            'prediction': result['best_model']['prediction'],
            'prediction_label': result['best_model']['prediction_label'],
            'confidence': result['best_model']['confidence'],
            'model_used': result['best_model']['name'],
            'all_models': result['all_models'],
            'risk_assessment': risk,
            'image_info': analysis_result['image_info'],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# APPOINTMENT ROUTES
# ============================================================================

@app.route('/appointments')
@login_required
def appointments():
    """Appointments booking page"""
    return render_template('appointments.html')

@app.route('/api/appointments/doctors')
@login_required
def api_get_doctors():
    """Get all doctors with locations"""
    try:
        doctors = appointment_manager.get_all_doctors()
        return jsonify({'doctors': doctors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/locations/<int:doctor_id>')
@login_required
def api_get_doctor_locations(doctor_id):
    """Get locations for a specific doctor"""
    try:
        locations = appointment_manager.get_doctor_locations(doctor_id)
        return jsonify({'locations': locations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/slots')
@login_required
def api_get_available_slots():
    """Get available time slots"""
    try:
        doctor_id = request.args.get('doctor_id', type=int)
        location_id = request.args.get('location_id', type=int)
        date = request.args.get('date')
        
        if not all([doctor_id, location_id, date]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        slots = appointment_manager.get_available_slots(doctor_id, location_id, date)
        return jsonify({'slots': slots})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/book', methods=['POST'])
@login_required
def api_book_appointment():
    """Book an appointment"""
    try:
        data = request.get_json()
        
        result = appointment_manager.book_appointment(
            patient_id=session['user_id'],
            doctor_id=data.get('doctor_id'),
            location_id=data.get('location_id'),
            appointment_date=data.get('appointment_date'),
            appointment_time=data.get('appointment_time'),
            reason=data.get('reason'),
            notes=data.get('notes')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/my')
@login_required
def api_get_my_appointments():
    """Get user's appointments"""
    try:
        appointments = appointment_manager.get_patient_appointments(session['user_id'])
        return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def api_cancel_appointment(appointment_id):
    """Cancel an appointment"""
    try:
        result = appointment_manager.cancel_appointment(appointment_id, session['user_id'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Doctor appointment management routes
@app.route('/api/doctor/appointments')
@doctor_required
def api_get_doctor_appointments():
    """Get doctor's appointments"""
    try:
        date = request.args.get('date')
        status = request.args.get('status')
        
        appointments = appointment_manager.get_doctor_appointments(
            session['user_id'], 
            date=date, 
            status=status
        )
        return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor/locations', methods=['GET', 'POST'])
@doctor_required
def api_doctor_locations():
    """Manage doctor locations"""
    if request.method == 'GET':
        try:
            locations = appointment_manager.get_doctor_locations(session['user_id'])
            return jsonify({'locations': locations})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            result = appointment_manager.add_location(
                doctor_id=session['user_id'],
                location_name=data.get('location_name'),
                address=data.get('address'),
                city=data.get('city'),
                phone=data.get('phone')
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/doctor/availability', methods=['GET', 'POST'])
@doctor_required
def api_doctor_availability():
    """Manage doctor availability"""
    if request.method == 'GET':
        try:
            location_id = request.args.get('location_id', type=int)
            availability = appointment_manager.get_doctor_availability(
                session['user_id'], 
                location_id=location_id
            )
            return jsonify({'availability': availability})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            result = appointment_manager.add_availability(
                doctor_id=session['user_id'],
                location_id=data.get('location_id'),
                day_of_week=data.get('day_of_week'),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                slot_duration=data.get('slot_duration', 30)
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Load models on startup
    predictor.load_models()
    
    # Create default admin account if not exists
    auth_manager.create_default_admin()
    
    # Run app
    print("=" * 50)
    print("🚀 Breast Cancer Detection System")
    print("=" * 50)
    print("Server running at: http://localhost:5000")
    print("Default Admin: admin / admin123")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Use Waitress for production-ready server (no warning)
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except ImportError:
        # Fallback to Flask dev server if Waitress not installed
        app.run(debug=True, host='0.0.0.0', port=5000)
