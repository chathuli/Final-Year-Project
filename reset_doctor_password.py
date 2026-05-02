"""
Reset doctor password for testing
"""
import sys
sys.path.insert(0, 'src')

from auth import AuthManager

auth_mgr = AuthManager()

# Reset password for doctor 'himaya'
username = 'himaya'
new_password = 'doctor123'

# Get user
doctors = auth_mgr.get_all_users(role='doctor')
doctor = next((d for d in doctors if d['username'] == username), None)

if doctor:
    result = auth_mgr.update_user(
        user_id=doctor['id'],
        password=new_password
    )
    
    if result['success']:
        print("=" * 60)
        print("Doctor Password Reset Successfully!")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Password: {new_password}")
        print(f"Full Name: {doctor['full_name']}")
        print(f"Email: {doctor['email']}")
        print("=" * 60)
        print("\nLogin at: http://localhost:5000/login/doctor")
    else:
        print(f"Error: {result.get('error')}")
else:
    print(f"Doctor '{username}' not found")
