"""
Make a user an admin
"""

import sqlite3

def make_user_admin(username):
    """Make a user an admin"""
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT id, username, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return
        
        user_id, username, current_role = user
        
        if current_role == 'admin':
            print(f"✅ User '{username}' is already an admin!")
            return
        
        # Update user role to admin
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (username,))
        conn.commit()
        
        print(f"✅ User '{username}' is now an admin!")
        print(f"   Previous role: {current_role}")
        print(f"   New role: admin")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username to make admin: ")
    
    make_user_admin(username)
