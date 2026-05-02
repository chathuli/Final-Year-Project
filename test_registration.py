"""
Test user registration to verify role assignment
"""
import sys
sys.path.insert(0, 'src')

from auth import AuthManager

auth_mgr = AuthManager()

print("=" * 60)
print("Testing User Registration System")
print("=" * 60)

# Test 1: Register a new user (should get 'user' role by default)
print("\n[TEST 1] Registering a new patient...")
result = auth_mgr.register_user(
    username='test_patient',
    email='patient@test.com',
    password='test123',
    full_name='Test Patient'
    # Note: No role parameter - should default to 'user'
)

if result['success']:
    print(f"✓ Registration successful! User ID: {result['user_id']}")
    
    # Verify the role
    users = auth_mgr.get_all_users()
    test_user = next((u for u in users if u['username'] == 'test_patient'), None)
    
    if test_user:
        print(f"\n[VERIFICATION]")
        print(f"Username: {test_user['username']}")
        print(f"Email: {test_user['email']}")
        print(f"Full Name: {test_user['full_name']}")
        print(f"Role: {test_user['role']}")
        print(f"Active: {test_user['is_active']}")
        
        if test_user['role'] == 'user':
            print("\n✓ SUCCESS: User was assigned 'user' role by default!")
        else:
            print(f"\n✗ ERROR: User has role '{test_user['role']}' instead of 'user'")
    else:
        print("\n✗ ERROR: Could not find registered user")
else:
    print(f"✗ Registration failed: {result.get('error')}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)

# Cleanup
print("\nCleaning up test user...")
import sqlite3
conn = sqlite3.connect('data/users.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM users WHERE username = 'test_patient'")
conn.commit()
conn.close()
print("✓ Test user removed")
