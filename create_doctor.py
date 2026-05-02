"""
Create a demo doctor account
"""
import sys
sys.path.insert(0, 'src')

from auth import AuthManager

auth_mgr = AuthManager()

# Check existing doctors
doctors = auth_mgr.get_all_users(role='doctor')

if doctors:
    print("Existing Doctor Accounts:")
    print("=" * 60)
    for doc in doctors:
        print(f"Username: {doc['username']}")
        print(f"Email: {doc['email']}")
        print(f"Full Name: {doc['full_name']}")
        print(f"Active: {'Yes' if doc['is_active'] else 'No'}")
        print("-" * 60)
else:
    print("No doctor accounts found. Creating demo doctor...")
    
    # Create demo doctor
    result = auth_mgr.register_user(
        username='doctor1',
        email='doctor1@hospital.com',
        password='doctor123',
        full_name='Dr. Sarah Johnson',
        role='doctor'
    )
    
    if result['success']:
        print("Demo doctor created successfully!")
        print("=" * 60)
        print("Username: doctor1")
        print("Password: doctor123")
        print("Email: doctor1@hospital.com")
        print("Full Name: Dr. Sarah Johnson")
        print("=" * 60)
    else:
        print(f"Error creating doctor: {result.get('error')}")

print("\nYou can use these credentials to login at:")
print("http://localhost:5000/login/doctor")
