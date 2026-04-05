import sqlite3

conn = sqlite3.connect('data/users.db')
cursor = conn.cursor()

# Update osandi's name
cursor.execute("""
    UPDATE users 
    SET full_name = 'Dr.Osandi Hirimuthugoda' 
    WHERE username = 'osandi'
""")

conn.commit()
print("✓ Updated osandi's name to 'Dr.Osandi Hirimuthugoda'")

# Verify the change
cursor.execute("SELECT username, full_name FROM users WHERE username = 'osandi'")
result = cursor.fetchone()
print(f"✓ Verified: {result[0]} -> {result[1]}")

conn.close()
