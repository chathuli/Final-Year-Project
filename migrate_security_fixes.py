"""
Migration script for security fixes
- Adds user_id column to predictions table
- Migrates existing passwords from SHA-256 to bcrypt
"""

import sqlite3
import bcrypt
import hashlib

def migrate_predictions_table():
    """Add user_id column to predictions table"""
    print("Migrating predictions table...")
    
    conn = sqlite3.connect('data/predictions.db')
    cursor = conn.cursor()
    
    try:
        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            # Add user_id column
            cursor.execute('ALTER TABLE predictions ADD COLUMN user_id INTEGER')
            conn.commit()
            print("✓ Added user_id column to predictions table")
        else:
            print("✓ user_id column already exists")
    
    except Exception as e:
        print(f"✗ Error migrating predictions table: {e}")
    finally:
        conn.close()

def migrate_user_passwords():
    """Migrate user passwords from SHA-256 to bcrypt"""
    print("\nMigrating user passwords to bcrypt...")
    
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    
    try:
        # Get all users
        cursor.execute("SELECT id, username, password_hash FROM users")
        users = cursor.fetchall()
        
        migrated_count = 0
        
        for user_id, username, old_hash in users:
            # Check if password is already bcrypt (starts with $2b$)
            if old_hash.startswith('$2b$'):
                print(f"  - {username}: already using bcrypt")
                continue
            
            # For known default passwords, migrate them
            # You should reset all user passwords after migration
            if username == 'admin':
                # Default admin password
                new_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
                migrated_count += 1
                print(f"  ✓ {username}: migrated to bcrypt (default password)")
            else:
                # For other users, we can't recover their original password
                # Set a temporary password that they must change
                temp_password = f"temp{user_id}123"
                new_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
                migrated_count += 1
                print(f"  ✓ {username}: migrated to bcrypt (temporary password: {temp_password})")
        
        conn.commit()
        print(f"\n✓ Migrated {migrated_count} user passwords")
        
        if migrated_count > 0:
            print("\n⚠️  IMPORTANT: Users with temporary passwords must change them on next login!")
    
    except Exception as e:
        print(f"✗ Error migrating passwords: {e}")
    finally:
        conn.close()

def create_env_template():
    """Create .env.template file for environment variables"""
    print("\nCreating .env.template...")
    
    template_content = """# Environment Variables Template
# Copy this file to .env and fill in your actual values

# Email Configuration (Gmail SMTP)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password

# Flask Secret Key (generate a random string)
SECRET_KEY=your-secret-key-here

# Database Paths (optional, defaults to data/ directory)
# USERS_DB_PATH=data/users.db
# PREDICTIONS_DB_PATH=data/predictions.db
# APPOINTMENTS_DB_PATH=data/appointments.db
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(template_content)
        print("✓ Created .env.template file")
        print("\n⚠️  Remember to:")
        print("   1. Copy .env.template to .env")
        print("   2. Fill in your actual credentials in .env")
        print("   3. Add .env to .gitignore")
    except Exception as e:
        print(f"✗ Error creating .env.template: {e}")

def update_gitignore():
    """Add .env to .gitignore if not already present"""
    print("\nUpdating .gitignore...")
    
    try:
        # Read existing .gitignore
        try:
            with open('.gitignore', 'r') as f:
                content = f.read()
        except FileNotFoundError:
            content = ""
        
        # Add .env if not present
        if '.env' not in content:
            with open('.gitignore', 'a') as f:
                if content and not content.endswith('\n'):
                    f.write('\n')
                f.write('\n# Environment variables\n.env\n')
            print("✓ Added .env to .gitignore")
        else:
            print("✓ .env already in .gitignore")
    
    except Exception as e:
        print(f"✗ Error updating .gitignore: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Security Migration Script")
    print("=" * 60)
    
    migrate_predictions_table()
    migrate_user_passwords()
    create_env_template()
    update_gitignore()
    
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install new dependencies: pip install bcrypt Flask-Limiter")
    print("2. Set environment variables (EMAIL_USER, EMAIL_PASSWORD)")
    print("3. Restart the Flask application")
    print("4. Notify users to change their passwords")
    print("=" * 60)
