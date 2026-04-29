"""
Database Migration Script
Adds new columns for symptom-based predictions
"""

import sqlite3
import os

def migrate_database(db_path='data/predictions.db'):
    """Add new columns to predictions table"""
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add prediction_type column if it doesn't exist
        if 'prediction_type' not in columns:
            print("Adding prediction_type column...")
            cursor.execute('''
                ALTER TABLE predictions 
                ADD COLUMN prediction_type TEXT DEFAULT 'manual'
            ''')
            print("✓ prediction_type column added")
        else:
            print("✓ prediction_type column already exists")
        
        # Add symptoms_data column if it doesn't exist
        if 'symptoms_data' not in columns:
            print("Adding symptoms_data column...")
            cursor.execute('''
                ALTER TABLE predictions 
                ADD COLUMN symptoms_data TEXT
            ''')
            print("✓ symptoms_data column added")
        else:
            print("✓ symptoms_data column already exists")
        
        # Add risk_assessment column if it doesn't exist
        if 'risk_assessment' not in columns:
            print("Adding risk_assessment column...")
            cursor.execute('''
                ALTER TABLE predictions 
                ADD COLUMN risk_assessment TEXT
            ''')
            print("✓ risk_assessment column added")
        else:
            print("✓ risk_assessment column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Migrate main database
    print("Migrating main database...")
    migrate_database('data/predictions.db')
    
    # Migrate src database if it exists
    if os.path.exists('src/data/predictions.db'):
        print("\nMigrating src database...")
        migrate_database('src/data/predictions.db')
    
    print("\n✅ All databases migrated!")
