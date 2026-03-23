import sqlite3
import os

def show_database_info(db_path, db_name):
    if not os.path.exists(db_path):
        print(f"\n❌ {db_name} not found at {db_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 DATABASE: {db_name}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📋 Tables: {len(tables)}")
    
    for table in tables:
        table_name = table[0]
        print(f"\n{'─'*60}")
        print(f"📁 TABLE: {table_name}")
        print(f"{'─'*60}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("\n🔧 Schema:")
        for col in columns:
            col_id, name, type_, notnull, default, pk = col
            pk_marker = " 🔑 PRIMARY KEY" if pk else ""
            null_marker = " NOT NULL" if notnull else ""
            default_marker = f" DEFAULT {default}" if default else ""
            print(f"  • {name}: {type_}{pk_marker}{null_marker}{default_marker}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total Records: {count}")
        
        # Show sample data (first 5 rows)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            
            print(f"\n📄 Sample Data (showing {min(count, 5)} of {count} records):")
            print()
            
            # Print column headers
            col_names = [col[1] for col in columns]
            header = " | ".join([f"{name[:15]:15}" for name in col_names])
            print(f"  {header}")
            print(f"  {'-' * len(header)}")
            
            # Print rows
            for row in rows:
                row_str = " | ".join([f"{str(val)[:15]:15}" for val in row])
                print(f"  {row_str}")
    
    conn.close()

# Show users database
show_database_info('data/users.db', 'users.db')

# Show predictions database
show_database_info('data/predictions.db', 'predictions.db')

print(f"\n{'='*60}")
print("✅ Database inspection complete!")
print(f"{'='*60}\n")
