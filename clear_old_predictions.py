"""
Clear old predictions with NULL/undefined values from the database
"""

import sqlite3
import os

def clear_old_predictions():
    db_path = 'data/predictions.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Count predictions with NULL values
    cursor.execute('''
        SELECT COUNT(*) FROM predictions 
        WHERE prediction_label IS NULL OR model_name IS NULL
    ''')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("✅ No old predictions found. Database is clean!")
        conn.close()
        return
    
    print(f"Found {count} predictions with undefined values")
    
    # Ask for confirmation
    response = input(f"Delete these {count} predictions? (yes/no): ").strip().lower()
    
    if response == 'yes':
        cursor.execute('''
            DELETE FROM predictions 
            WHERE prediction_label IS NULL OR model_name IS NULL
        ''')
        conn.commit()
        print(f"✅ Deleted {count} old predictions")
        print("✅ Database cleaned successfully!")
    else:
        print("❌ Operation cancelled")
    
    conn.close()

if __name__ == '__main__':
    clear_old_predictions()
