"""Test appointments API"""
import sqlite3

# Check users
print("=== USERS (Doctors) ===")
conn = sqlite3.connect('data/users.db')
cursor = conn.cursor()
cursor.execute("SELECT id, username, full_name, role FROM users WHERE role='doctor'")
doctors = cursor.fetchall()
for doc in doctors:
    print(f"ID: {doc[0]}, Username: {doc[1]}, Name: {doc[2]}, Role: {doc[3]}")
conn.close()

# Check locations
print("\n=== DOCTOR LOCATIONS ===")
conn = sqlite3.connect('data/appointments.db')
cursor = conn.cursor()
cursor.execute("SELECT doctor_id, location_name, city FROM doctor_locations")
locations = cursor.fetchall()
for loc in locations:
    print(f"Doctor ID: {loc[0]}, Location: {loc[1]}, City: {loc[2]}")

# Check availability
print("\n=== DOCTOR AVAILABILITY ===")
cursor.execute("SELECT doctor_id, location_id, day_of_week, start_time, end_time FROM doctor_availability LIMIT 5")
avail = cursor.fetchall()
for av in avail:
    print(f"Doctor ID: {av[0]}, Location ID: {av[1]}, Day: {av[2]}, Time: {av[3]}-{av[4]}")
conn.close()

# Test the API
print("\n=== TESTING API ===")
from src.appointments import AppointmentManager
am = AppointmentManager()
doctors = am.get_all_doctors()
print(f"API returned {len(doctors)} doctors:")
for d in doctors:
    print(f"  - {d}")
