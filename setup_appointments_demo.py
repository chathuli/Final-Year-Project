"""
Setup demo data for appointments system
Creates sample locations and availability for testing
"""

from src.appointments import AppointmentManager
from src.auth import AuthManager

def setup_demo_data():
    """Setup demo appointments data"""
    
    appointment_mgr = AppointmentManager()
    auth_mgr = AuthManager()
    
    print("=" * 60)
    print("🏥 Setting Up Appointments Demo Data")
    print("=" * 60)
    
    # Get all doctors
    doctors = auth_mgr.get_all_users(role='doctor')
    
    if not doctors:
        print("❌ No doctors found. Please create a doctor account first.")
        print("   Login as admin and register a doctor from the admin panel.")
        return
    
    print(f"\n✅ Found {len(doctors)} doctor(s)")
    
    for doctor in doctors:
        print(f"\n📋 Setting up data for Dr. {doctor['full_name']}...")
        
        # Add locations
        locations = [
            {
                'location_name': 'City Hospital - Main Branch',
                'address': '123 Medical Center Drive',
                'city': 'Colombo',
                'phone': '+94 11 234 5678'
            },
            {
                'location_name': 'Suburban Clinic',
                'address': '456 Health Street',
                'city': 'Kandy',
                'phone': '+94 81 234 5678'
            }
        ]
        
        location_ids = []
        for loc in locations:
            result = appointment_mgr.add_location(
                doctor_id=doctor['id'],
                **loc
            )
            if result['success']:
                location_ids.append(result['location_id'])
                print(f"   ✅ Added location: {loc['location_name']}")
        
        # Add availability for each location
        # Days: 0=Monday, 1=Tuesday, ..., 6=Sunday
        schedules = [
            {'day': 1, 'start': '09:00', 'end': '12:00'},  # Tuesday morning
            {'day': 1, 'start': '14:00', 'end': '17:00'},  # Tuesday afternoon
            {'day': 3, 'start': '09:00', 'end': '12:00'},  # Thursday morning
            {'day': 3, 'start': '14:00', 'end': '17:00'},  # Thursday afternoon
            {'day': 5, 'start': '09:00', 'end': '13:00'},  # Saturday morning
        ]
        
        for location_id in location_ids:
            for schedule in schedules:
                result = appointment_mgr.add_availability(
                    doctor_id=doctor['id'],
                    location_id=location_id,
                    day_of_week=schedule['day'],
                    start_time=schedule['start'],
                    end_time=schedule['end'],
                    slot_duration=30
                )
                if result['success']:
                    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                    print(f"   ✅ Added schedule: {day_names[schedule['day']]} {schedule['start']}-{schedule['end']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo Data Setup Complete!")
    print("=" * 60)
    print("\n📌 Next Steps:")
    print("   1. Start the application: python src/app.py")
    print("   2. Login as a user")
    print("   3. Go to Appointments page")
    print("   4. Book an appointment!")
    print("\n💡 Available Days:")
    print("   - Tuesday: 9:00 AM - 12:00 PM, 2:00 PM - 5:00 PM")
    print("   - Thursday: 9:00 AM - 12:00 PM, 2:00 PM - 5:00 PM")
    print("   - Saturday: 9:00 AM - 1:00 PM")
    print("=" * 60)

if __name__ == '__main__':
    setup_demo_data()
