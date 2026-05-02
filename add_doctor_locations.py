"""
Add locations and availability for Dr. Himaya Pieris
"""
import sys
sys.path.insert(0, 'src')

from appointments import AppointmentManager
from auth import AuthManager

auth_mgr = AuthManager()
appointment_mgr = AppointmentManager()

print("=" * 70)
print("Adding Locations for Dr. Himaya Pieris")
print("=" * 70)

# Find Dr. Himaya
doctors = auth_mgr.get_all_users(role='doctor')
himaya = next((d for d in doctors if d['username'] == 'himaya'), None)

if not himaya:
    print("Error: Dr. Himaya not found!")
    sys.exit(1)

print(f"\nFound: {himaya['full_name']} (ID: {himaya['id']})")
print("\nAdding locations...")

# Location 1: Colombo Main Hospital
location1 = appointment_mgr.add_location(
    doctor_id=himaya['id'],
    location_name='Colombo General Hospital',
    address='Regent Street, Colombo 08',
    city='Colombo',
    phone='+94 11 269 1111'
)

if location1['success']:
    print(f"✓ Location 1 added: Colombo General Hospital (ID: {location1['location_id']})")
    
    # Add availability for Location 1
    schedules = [
        {'day': 1, 'start': '09:00', 'end': '12:00'},  # Tuesday morning
        {'day': 1, 'start': '14:00', 'end': '17:00'},  # Tuesday afternoon
        {'day': 3, 'start': '09:00', 'end': '12:00'},  # Thursday morning
    ]
    
    for schedule in schedules:
        result = appointment_mgr.add_availability(
            doctor_id=himaya['id'],
            location_id=location1['location_id'],
            day_of_week=schedule['day'],
            start_time=schedule['start'],
            end_time=schedule['end'],
            slot_duration=30
        )
        if result['success']:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            print(f"  ✓ {days[schedule['day']]} {schedule['start']}-{schedule['end']}")

# Location 2: Kandy Teaching Hospital
location2 = appointment_mgr.add_location(
    doctor_id=himaya['id'],
    location_name='Kandy Teaching Hospital',
    address='William Gopallawa Mawatha, Kandy',
    city='Kandy',
    phone='+94 81 223 3337'
)

if location2['success']:
    print(f"\n✓ Location 2 added: Kandy Teaching Hospital (ID: {location2['location_id']})")
    
    # Add availability for Location 2
    schedules = [
        {'day': 2, 'start': '09:00', 'end': '13:00'},  # Wednesday morning
        {'day': 4, 'start': '14:00', 'end': '18:00'},  # Friday afternoon
    ]
    
    for schedule in schedules:
        result = appointment_mgr.add_availability(
            doctor_id=himaya['id'],
            location_id=location2['location_id'],
            day_of_week=schedule['day'],
            start_time=schedule['start'],
            end_time=schedule['end'],
            slot_duration=30
        )
        if result['success']:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            print(f"  ✓ {days[schedule['day']]} {schedule['start']}-{schedule['end']}")

# Location 3: Galle Private Clinic
location3 = appointment_mgr.add_location(
    doctor_id=himaya['id'],
    location_name='Himaya Medical Center - Galle',
    address='No. 45, Matara Road, Galle',
    city='Galle',
    phone='+94 91 222 4567'
)

if location3['success']:
    print(f"\n✓ Location 3 added: Himaya Medical Center - Galle (ID: {location3['location_id']})")
    
    # Add availability for Location 3
    schedules = [
        {'day': 5, 'start': '09:00', 'end': '13:00'},  # Saturday morning
        {'day': 5, 'start': '14:00', 'end': '17:00'},  # Saturday afternoon
    ]
    
    for schedule in schedules:
        result = appointment_mgr.add_availability(
            doctor_id=himaya['id'],
            location_id=location3['location_id'],
            day_of_week=schedule['day'],
            start_time=schedule['start'],
            end_time=schedule['end'],
            slot_duration=30
        )
        if result['success']:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            print(f"  ✓ {days[schedule['day']]} {schedule['start']}-{schedule['end']}")

print("\n" + "=" * 70)
print("Setup Complete!")
print("=" * 70)
print("\nDr. Himaya Pieris now has 3 locations:")
print("1. Colombo General Hospital - Tue & Thu")
print("2. Kandy Teaching Hospital - Wed & Fri")
print("3. Himaya Medical Center, Galle - Saturday")
print("\nPatients can now book appointments at any of these locations!")
print("=" * 70)
