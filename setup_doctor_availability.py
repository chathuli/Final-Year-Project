"""
Quick setup script to add locations and availability for registered doctors
"""
from src.appointments import AppointmentManager
from src.auth import AuthManager

def setup_doctors():
    auth = AuthManager()
    appt = AppointmentManager()
    
    # Get all doctors
    doctors = auth.get_all_users(role='doctor')
    
    if not doctors:
        print("No doctors found. Please register doctors first from admin panel.")
        return
    
    print(f"Found {len(doctors)} doctor(s)")
    print("=" * 60)
    
    for doctor in doctors:
        print(f"\nSetting up: {doctor['full_name']} (ID: {doctor['id']})")
        
        # Add sample locations
        locations = [
            {
                'location_name': 'Main Hospital - Oncology Department',
                'address': '123 Medical Center Drive',
                'city': 'Colombo',
                'phone': '+94 11 234 5678'
            },
            {
                'location_name': 'City Clinic - Cancer Care Unit',
                'address': '456 Health Street',
                'city': 'Kandy',
                'phone': '+94 81 234 5678'
            }
        ]
        
        location_ids = []
        for loc in locations:
            result = appt.add_location(
                doctor_id=doctor['id'],
                location_name=loc['location_name'],
                address=loc['address'],
                city=loc['city'],
                phone=loc['phone']
            )
            if result['success']:
                location_ids.append(result['location_id'])
                print(f"  + Added location: {loc['location_name']}")
        
        # Add availability for each location
        # Monday to Friday, 9 AM to 5 PM
        for location_id in location_ids:
            for day in range(5):  # 0=Monday to 4=Friday
                result = appt.add_availability(
                    doctor_id=doctor['id'],
                    location_id=location_id,
                    day_of_week=day,
                    start_time='09:00',
                    end_time='17:00',
                    slot_duration=30
                )
                if result['success']:
                    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                    print(f"  + Added availability: {day_names[day]} 9:00-17:00")
    
    print("\n" + "=" * 60)
    print("Setup complete! Doctors are now available for appointments.")
    print("=" * 60)

if __name__ == '__main__':
    setup_doctors()
