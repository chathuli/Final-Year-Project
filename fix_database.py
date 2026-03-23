"""
Fix database schema - Add missing created_by column
"""

import sqlite3
import os

def fix_users_table():
    """Add created_by column to users table"""
    db_path = os.path.join('data', 'users.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found at:", db_path)
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'created_by' not in columns:
            print("Adding created_by column...")
            cursor.execute('''
                ALTER TABLE users 
                ADD COLUMN created_by INTEGER
            ''')
            conn.commit()
            print("✅ Successfully added created_by column")
        else:
            print("✅ created_by column already exists")
        
        # Show current schema
        print("\n📋 Current users table schema:")
        cursor.execute("PRAGMA table_info(users)")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("🔧 Fixing Database Schema")
    print("=" * 50)
    fix_users_table()
    print("=" * 50)
    print("✅ Done! You can now register doctors.")
    print("=" * 50)
