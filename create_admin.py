"""
Create or reset admin account
"""
import sys
sys.path.insert(0, 'src')

from auth import AuthManager

auth_mgr = AuthManager()

# Check if admin exists
admins = auth_mgr.get_all_users(role='admin')

if admins:
    print("Existing Admin Accounts:")
    print("=" * 60)
    for admin in admins:
        print(f"Username: {admin['username']}")
        print(f"Email: {admin['email']}")
        print(f"Full Name: {admin['full_name']}")
        print("-" * 60)
    
    # Reset first admin password
    admin = admins[0]
    result = auth_mgr.update_user(
        user_id=admin['id'],
        password='admin123'
    )
    
    if result['success']:
        print("\nAdmin password reset successfully!")
        print("=" * 60)
        print(f"Username: {admin['username']}")
        print("Password: admin123")
        print("=" * 60)
else:
    print("No admin account found. Creating default admin...")
    
    # Create default admin
    result = auth_mgr.register_user(
        username='admin',
        email='admin@hospital.com',
        password='admin123',
        full_name='System Administrator',
        role='admin'
    )
    
    if result['success']:
        print("Admin account created successfully!")
        print("=" * 60)
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@hospital.com")
        print("=" * 60)
    else:
        print(f"Error creating admin: {result.get('error')}")

print("\nLogin at: http://localhost:5000/login/admin")
print("Or use unified login: http://localhost:5000/login")
