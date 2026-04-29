"""
Database module for storing prediction history
"""

import sqlite3
import json
from datetime import datetime
import os

class PredictionDatabase:
    def __init__(self, db_path='data/predictions.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA busy_timeout=5000')  # Wait up to 5 seconds if locked
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enable WAL mode once during initialization
        try:
            cursor.execute('PRAGMA journal_mode=WAL')
        except:
            pass  # Ignore if already in WAL mode
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prediction INTEGER,
                prediction_label TEXT,
                confidence REAL,
                model_name TEXT,
                features TEXT,
                all_model_predictions TEXT,
                prediction_type TEXT DEFAULT 'manual',
                symptoms_data TEXT,
                risk_assessment TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_prediction(self, prediction, confidence, model_name, features, all_predictions=None, prediction_type='manual', symptoms_data=None, risk_assessment=None):
        """Save a prediction to the database"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            prediction_label = 'Malignant' if prediction == 1 else 'Benign'
            features_json = json.dumps(features)
            all_predictions_json = json.dumps(all_predictions) if all_predictions else None
            symptoms_json = json.dumps(symptoms_data) if symptoms_data else None
            risk_json = json.dumps(risk_assessment) if risk_assessment else None
            
            cursor.execute('''
                INSERT INTO predictions 
                (prediction, prediction_label, confidence, model_name, features, all_model_predictions, prediction_type, symptoms_data, risk_assessment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (prediction, prediction_label, confidence, model_name, features_json, all_predictions_json, prediction_type, symptoms_json, risk_json))
            
            prediction_id = cursor.lastrowid
            conn.commit()
            
            return prediction_id
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all_predictions(self, limit=100):
        """Get all predictions from database"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, prediction_label, confidence, model_name, prediction_type, symptoms_data, risk_assessment
                FROM predictions
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            predictions = []
            for row in cursor.fetchall():
                pred = {
                    'id': row[0],
                    'timestamp': row[1],
                    'prediction_label': row[2],
                    'confidence': row[3],
                    'model_name': row[4],
                    'prediction_type': row[5] if row[5] else 'manual'
                }
                
                # Add symptom data if available
                if row[6]:
                    pred['symptoms_data'] = json.loads(row[6])
                
                # Add risk assessment if available
                if row[7]:
                    pred['risk_assessment'] = json.loads(row[7])
                
                predictions.append(pred)
            
            return predictions
        except Exception as e:
            print(f"Error getting predictions: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_statistics(self):
        """Get prediction statistics"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total predictions
            cursor.execute('SELECT COUNT(*) FROM predictions')
            total = cursor.fetchone()[0]
            
            # Benign count
            cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction_label = 'Benign'")
            benign = cursor.fetchone()[0]
            
            # Malignant count
            cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction_label = 'Malignant'")
            malignant = cursor.fetchone()[0]
            
            # Average confidence
            cursor.execute('SELECT AVG(confidence) FROM predictions')
            avg_confidence = cursor.fetchone()[0] or 0
            
            # Predictions by date (last 7 days)
            cursor.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) as count
                FROM predictions
                WHERE timestamp >= datetime('now', '-7 days')
                GROUP BY DATE(timestamp)
                ORDER BY date
            ''')
            daily_predictions = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            return {
                'total': total,
                'benign': benign,
                'malignant': malignant,
                'avg_confidence': round(avg_confidence * 100, 2),
                'daily_predictions': daily_predictions
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total': 0,
                'benign': 0,
                'malignant': 0,
                'avg_confidence': 0,
                'daily_predictions': []
            }
        finally:
            if conn:
                conn.close()
    
    def get_prediction_by_id(self, prediction_id):
        """Get a specific prediction by ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, prediction, prediction_label, confidence, 
                       model_name, features, all_model_predictions, prediction_type, symptoms_data, risk_assessment
                FROM predictions
                WHERE id = ?
            ''', (prediction_id,))
            
            row = cursor.fetchone()
            
            if row:
                pred = {
                    'id': row[0],
                    'timestamp': row[1],
                    'prediction': row[2],
                    'prediction_label': row[3],
                    'confidence': row[4],
                    'model_name': row[5],
                    'features': json.loads(row[6]),
                    'all_model_predictions': json.loads(row[7]) if row[7] else None,
                    'prediction_type': row[8] if row[8] else 'manual'
                }
                
                # Add symptom data if available
                if row[9]:
                    pred['symptoms_data'] = json.loads(row[9])
                
                # Add risk assessment if available
                if row[10]:
                    pred['risk_assessment'] = json.loads(row[10])
                
                return pred
            return None
        except Exception as e:
            print(f"Error getting prediction by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    
    def delete_prediction(self, prediction_id):
        """Delete a prediction by ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM predictions WHERE id = ?', (prediction_id,))
            conn.commit()
            
            return {
                'success': True,
                'message': f'Prediction #{prediction_id} deleted successfully'
            }
        except Exception as e:
            print(f"Error deleting prediction: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if conn:
                conn.close()
