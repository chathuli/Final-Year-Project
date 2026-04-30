"""
Reset user password
"""
import sqlite3
import hashlib

def reset_password(username, new_password):
    """Reset password for a user"""
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    
    # Hash the new password
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    
    # Update the password
    cursor.execute('''
        UPDATE users 
        SET password_hash = ? 
        WHERE username = ?
    ''', (password_hash, username))
    
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✅ Password reset successfully for user: {username}")
        print(f"   New password: {new_password}")
        return True
    else:
        print(f"❌ User not found: {username}")
        return False
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("PASSWORD RESET TOOL")
    print("=" * 60)
    
    # Reset passwords for common accounts
    accounts = [
        ("Amaraweera", "password123"),
        ("admin", "admin123"),
        ("osandi", "doctor123"),
    ]
    
    print("\nResetting passwords...\n")
    
    for username, password in accounts:
        reset_password(username, password)
    
    print("\n" + "=" * 60)
    print("TEST ACCOUNTS:")
    print("=" * 60)
    print("\n1. Regular User:")
    print("   Username: Amaraweera")
    print("   Password: password123")
    print("\n2. Admin:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n3. Doctor:")
    print("   Username: osandi")
    print("   Password: doctor123")
    print("\n" + "=" * 60)
    print("\nYou can now login with these credentials!")
    print("=" * 60)
