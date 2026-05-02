"""
Audit Logging Module
Tracks all important system activities for security, compliance, and debugging
"""

import sqlite3
import os
from datetime import datetime
from flask import request, session

class AuditLogger:
    """Manages audit logging for the system"""
    
    def __init__(self, db_path=None):
        """Initialize audit logger"""
        if db_path is None:
            # Use absolute path relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, 'data', 'audit.db')
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA busy_timeout=5000')
        return conn
    
    def init_database(self):
        """Initialize audit log database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enable WAL mode
        try:
            cursor.execute('PRAGMA journal_mode=WAL')
        except:
            pass
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                action TEXT NOT NULL,
                resource TEXT,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_user_id 
            ON audit_log(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_action 
            ON audit_log(action)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp 
            ON audit_log(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_status 
            ON audit_log(status)
        ''')
        
        conn.commit()
        conn.close()
        print("[OK] Audit log database initialized")
    
    def log(self, action, resource=None, details=None, status='SUCCESS', 
            error_message=None, user_id=None, username=None):
        """
        Log an audit event
        
        Args:
            action: Action performed (LOGIN, LOGOUT, PREDICT, DELETE, etc.)
            resource: Resource affected (prediction_id, user_id, etc.)
            details: Additional details about the action
            status: SUCCESS, FAILED, ERROR
            error_message: Error message if status is FAILED or ERROR
            user_id: User ID (auto-detected from session if not provided)
            username: Username (auto-detected from session if not provided)
        """
        conn = None
        try:
            # Get user info from session if not provided
            if user_id is None and hasattr(session, 'get'):
                user_id = session.get('user_id')
            if username is None and hasattr(session, 'get'):
                username = session.get('username')
            
            # Get request info if available
            ip_address = None
            user_agent = None
            if request:
                ip_address = request.remote_addr
                user_agent = request.headers.get('User-Agent', '')[:200]  # Limit length
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO audit_log 
                (user_id, username, action, resource, details, ip_address, 
                 user_agent, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, action, resource, details, ip_address, 
                  user_agent, status, error_message))
            
            conn.commit()
            
        except Exception as e:
            print(f"[AUDIT] Failed to log event: {e}")
            # Don't raise exception - audit logging should never break the app
        finally:
            if conn:
                conn.close()
    
    # Convenience methods for common actions
    
    def log_login(self, user_id, username, success=True, error=None):
        """Log user login attempt"""
        self.log(
            action='LOGIN',
            user_id=user_id,
            username=username,
            status='SUCCESS' if success else 'FAILED',
            error_message=error
        )
    
    def log_logout(self, user_id, username):
        """Log user logout"""
        self.log(
            action='LOGOUT',
            user_id=user_id,
            username=username,
            status='SUCCESS'
        )
    
    def log_prediction(self, user_id, username, prediction_id, result, confidence):
        """Log prediction made"""
        self.log(
            action='PREDICTION',
            resource=f'prediction_{prediction_id}',
            details=f'Result: {result}, Confidence: {confidence:.2f}%',
            user_id=user_id,
            username=username,
            status='SUCCESS'
        )
    
    def log_prediction_error(self, user_id, username, error):
        """Log prediction error"""
        self.log(
            action='PREDICTION',
            user_id=user_id,
            username=username,
            status='ERROR',
            error_message=str(error)
        )
    
    def log_data_access(self, user_id, username, resource, action='VIEW'):
        """Log data access (view, download, etc.)"""
        self.log(
            action=f'DATA_{action}',
            resource=resource,
            user_id=user_id,
            username=username,
            status='SUCCESS'
        )
    
    def log_data_deletion(self, user_id, username, resource):
        """Log data deletion"""
        self.log(
            action='DELETE',
            resource=resource,
            user_id=user_id,
            username=username,
            status='SUCCESS'
        )
    
    def log_admin_action(self, user_id, username, action, resource, details=None):
        """Log administrative action"""
        self.log(
            action=f'ADMIN_{action}',
            resource=resource,
            details=details,
            user_id=user_id,
            username=username,
            status='SUCCESS'
        )
    
    def log_password_change(self, user_id, username, success=True):
        """Log password change"""
        self.log(
            action='PASSWORD_CHANGE',
            user_id=user_id,
            username=username,
            status='SUCCESS' if success else 'FAILED'
        )
    
    def log_validation_error(self, user_id, username, error):
        """Log input validation error"""
        self.log(
            action='VALIDATION_ERROR',
            user_id=user_id,
            username=username,
            status='FAILED',
            error_message=str(error)
        )
    
    # Query methods
    
    def get_recent_logs(self, limit=100, user_id=None, action=None, status=None):
        """Get recent audit logs with optional filters"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM audit_log WHERE 1=1'
            params = []
            
            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)
            
            if action:
                query += ' AND action = ?'
                params.append(action)
            
            if status:
                query += ' AND status = ?'
                params.append(status)
            
            query += ' ORDER BY timestamp DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            logs = [dict(row) for row in cursor.fetchall()]
            
            return logs
        
        except Exception as e:
            print(f"[AUDIT] Error getting logs: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_failed_logins(self, hours=24, limit=100):
        """Get failed login attempts in the last N hours"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM audit_log
                WHERE action = 'LOGIN' 
                AND status = 'FAILED'
                AND timestamp >= datetime('now', '-' || ? || ' hours')
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (hours, limit))
            
            logs = [dict(row) for row in cursor.fetchall()]
            return logs
        
        except Exception as e:
            print(f"[AUDIT] Error getting failed logins: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_user_activity(self, user_id, limit=50):
        """Get activity for a specific user"""
        return self.get_recent_logs(limit=limit, user_id=user_id)
    
    def get_statistics(self, days=7):
        """Get audit log statistics"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total events
            cursor.execute('''
                SELECT COUNT(*) FROM audit_log
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
            ''', (days,))
            total_events = cursor.fetchone()[0]
            
            # Events by action
            cursor.execute('''
                SELECT action, COUNT(*) as count
                FROM audit_log
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
                GROUP BY action
                ORDER BY count DESC
            ''', (days,))
            by_action = dict(cursor.fetchall())
            
            # Events by status
            cursor.execute('''
                SELECT status, COUNT(*) as count
                FROM audit_log
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
                GROUP BY status
            ''', (days,))
            by_status = dict(cursor.fetchall())
            
            # Most active users
            cursor.execute('''
                SELECT username, COUNT(*) as count
                FROM audit_log
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
                AND username IS NOT NULL
                GROUP BY username
                ORDER BY count DESC
                LIMIT 10
            ''', (days,))
            top_users = [{'username': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Failed events
            cursor.execute('''
                SELECT COUNT(*) FROM audit_log
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
                AND status IN ('FAILED', 'ERROR')
            ''', (days,))
            failed_events = cursor.fetchone()[0]
            
            return {
                'total_events': total_events,
                'by_action': by_action,
                'by_status': by_status,
                'top_users': top_users,
                'failed_events': failed_events,
                'days': days
            }
        
        except Exception as e:
            print(f"[AUDIT] Error getting statistics: {e}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def search_logs(self, search_term, limit=100):
        """Search audit logs"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            search_pattern = f'%{search_term}%'
            
            cursor.execute('''
                SELECT * FROM audit_log
                WHERE username LIKE ? 
                OR action LIKE ?
                OR resource LIKE ?
                OR details LIKE ?
                OR error_message LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (search_pattern, search_pattern, search_pattern, 
                  search_pattern, search_pattern, limit))
            
            logs = [dict(row) for row in cursor.fetchall()]
            return logs
        
        except Exception as e:
            print(f"[AUDIT] Error searching logs: {e}")
            return []
        finally:
            if conn:
                conn.close()


# Global audit logger instance
_audit_logger = None

def get_audit_logger():
    """Get global audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
