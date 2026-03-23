"""
User Authentication Module
Handles user registration, login, and session management
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, request, jsonify

class AuthManager:
    def __init__(self, db_path='data/users.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA busy_timeout=5000')  # Wait up to 5 seconds if locked
        return conn
    
    def init_database(self):
        """Initialize users database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enable WAL mode once during initialization
        try:
            cursor.execute('PRAGMA journal_mode=WAL')
        except:
            pass  # Ignore if already in WAL mode
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # API tokens table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                last_used TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        
        # Create default admin if not exists
        self.create_default_admin(conn)
        
        conn.close()
    
    def create_default_admin(self, conn=None):
        """Create default admin user if not exists"""
        should_close = False
        if conn is None:
            conn = self.get_connection()
            should_close = True
        
        try:
            cursor = conn.cursor()
            
            # Check if admin user exists
            cursor.execute("SELECT id, role FROM users WHERE username = 'admin'")
            admin_user = cursor.fetchone()
            
            if admin_user is None:
                # Create default admin
                password_hash = self.hash_password('admin123')  # Change this!
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', 'admin@hospital.com', password_hash, 'System Administrator', 'admin'))
                conn.commit()
                print("✅ Default admin created: username='admin', password='admin123'")
            elif admin_user[1] != 'admin':
                # Update existing admin user to have admin role
                cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
                conn.commit()
                print("✅ Updated existing admin user to have admin role")
        finally:
            if should_close:
                conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_token(self):
        """Generate secure random token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username, email, password, full_name=None, role='user', created_by=None):
        """Register a new user"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, role, created_by))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            return {'success': True, 'user_id': user_id, 'message': 'User registered successfully'}
        
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'error': 'Username already exists'}
            elif 'email' in str(e):
                return {'success': False, 'error': 'Email already exists'}
            else:
                return {'success': False, 'error': 'Registration failed'}
        except Exception as e:
            return {'success': False, 'error': f'Database error: {str(e)}'}
        finally:
            if conn:
                conn.close()
    
    def get_all_users(self, role=None):
        """Get all users, optionally filtered by role"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if role:
                cursor.execute('''
                    SELECT id, username, email, full_name, role, created_at, last_login, is_active
                    FROM users WHERE role = ?
                    ORDER BY created_at DESC
                ''', (role,))
            else:
                cursor.execute('''
                    SELECT id, username, email, full_name, role, created_at, last_login, is_active
                    FROM users
                    ORDER BY created_at DESC
                ''')
            
            users = [dict(row) for row in cursor.fetchall()]
            return users
        
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def toggle_user_status(self, user_id):
        """Activate/deactivate a user"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET is_active = 1 - is_active
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if conn:
                conn.close()
    
    def login_user(self, username, password):
        """Authenticate user and create session"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user['id'],))
                
                conn.commit()
                
                return {
                    'success': True,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'full_name': user['full_name'],
                        'role': user['role']
                    }
                }
            else:
                return {'success': False, 'error': 'Invalid username or password'}
        
        except Exception as e:
            return {'success': False, 'error': f'Database error: {str(e)}'}
        finally:
            if conn:
                conn.close()
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if user:
                return dict(user)
            return None
        
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def create_api_token(self, user_id, name=None, expires_days=365):
        """Create API token for user"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            token = self.generate_token()
            expires_at = datetime.now() + timedelta(days=expires_days)
            
            cursor.execute('''
                INSERT INTO api_tokens (user_id, token, name, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, token, name, expires_at))
            
            conn.commit()
            token_id = cursor.lastrowid
            
            return {'success': True, 'token': token, 'token_id': token_id}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if conn:
                conn.close()
    
    def verify_api_token(self, token):
        """Verify API token and return user"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT t.*, u.username, u.email, u.role
                FROM api_tokens t
                JOIN users u ON t.user_id = u.id
                WHERE t.token = ? AND t.is_active = 1 
                AND (t.expires_at IS NULL OR t.expires_at > CURRENT_TIMESTAMP)
            ''', (token,))
            
            result = cursor.fetchone()
            
            if result:
                # Update last used
                cursor.execute('''
                    UPDATE api_tokens SET last_used = CURRENT_TIMESTAMP
                    WHERE token = ?
                ''', (token,))
                conn.commit()
                
                return {
                    'valid': True,
                    'user': {
                        'id': result['user_id'],
                        'username': result['username'],
                        'email': result['email'],
                        'role': result['role']
                    }
                }
            else:
                return {'valid': False, 'error': 'Invalid or expired token'}
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}
        finally:
            if conn:
                conn.close()
    
    def get_user_tokens(self, user_id):
        """Get all API tokens for a user"""
        conn = None
        try:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, created_at, expires_at, last_used, is_active
                FROM api_tokens
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            
            tokens = [dict(row) for row in cursor.fetchall()]
            
            return tokens
        
        except Exception as e:
            print(f"Error getting tokens: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def revoke_token(self, token_id, user_id):
        """Revoke an API token"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE api_tokens SET is_active = 0
                WHERE id = ? AND user_id = ?
            ''', (token_id, user_id))
            
            conn.commit()
            
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if conn:
                conn.close()


# Decorators for route protection
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific role(s) for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login', next=request.url))
            
            # Get user role
            auth_manager = AuthManager()
            user = auth_manager.get_user_by_id(session['user_id'])
            
            if not user or user['role'] not in roles:
                from flask import abort
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role"""
    return role_required('admin')(f)


def doctor_required(f):
    """Decorator to require doctor or admin role"""
    return role_required('doctor', 'admin')(f)


def api_token_required(f):
    """Decorator to require API token for API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for token in header
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify token
        auth_manager = AuthManager()
        result = auth_manager.verify_api_token(token)
        
        if not result['valid']:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request
        request.current_user = result['user']
        
        return f(*args, **kwargs)
    return decorated_function
