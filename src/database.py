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
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prediction INTEGER,
                prediction_label TEXT,
                confidence REAL,
                model_name TEXT,
                features TEXT,
                all_model_predictions TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_prediction(self, prediction, confidence, model_name, features, all_predictions=None):
        """Save a prediction to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        prediction_label = 'Malignant' if prediction == 1 else 'Benign'
        features_json = json.dumps(features)
        all_predictions_json = json.dumps(all_predictions) if all_predictions else None
        
        cursor.execute('''
            INSERT INTO predictions 
            (prediction, prediction_label, confidence, model_name, features, all_model_predictions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (prediction, prediction_label, confidence, model_name, features_json, all_predictions_json))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prediction_id
    
    def get_all_predictions(self, limit=100):
        """Get all predictions from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, prediction_label, confidence, model_name
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        predictions = []
        for row in cursor.fetchall():
            predictions.append({
                'id': row[0],
                'timestamp': row[1],
                'prediction': row[2],
                'confidence': row[3],
                'model': row[4]
            })
        
        conn.close()
        return predictions
    
    def get_statistics(self):
        """Get prediction statistics"""
        conn = sqlite3.connect(self.db_path)
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
        
        conn.close()
        
        return {
            'total': total,
            'benign': benign,
            'malignant': malignant,
            'avg_confidence': round(avg_confidence * 100, 2),
            'daily_predictions': daily_predictions
        }
    
    def get_prediction_by_id(self, prediction_id):
        """Get a specific prediction by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, prediction, prediction_label, confidence, 
                   model_name, features, all_model_predictions
            FROM predictions
            WHERE id = ?
        ''', (prediction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'timestamp': row[1],
                'prediction': row[2],
                'prediction_label': row[3],
                'confidence': row[4],
                'model_name': row[5],
                'features': json.loads(row[6]),
                'all_model_predictions': json.loads(row[7]) if row[7] else None
            }
        return None
