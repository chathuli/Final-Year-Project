# 📅 Doctor Appointments System

## ✅ Implementation Complete!

A complete appointment booking system with:
- Multi-location support for doctors
- Flexible scheduling system
- User-friendly booking wizard
- Appointment management
- Double-booking prevention

---

## Quick Setup

### 1. Run Demo Data Script
```bash
python setup_appointments_demo.py
```

This creates:
- Sample locations for all doctors
- Weekly availability schedules
- Time slots (30-minute intervals)

### 2. Access the System
```
URL: http://localhost:5000/appointments
```

---

## For Patients

### How to Book an Appointment

1. **Login** to the system
2. Go to **Appointments** page
3. **Select a Doctor** from the list
4. **Choose a Location** (hospital/clinic)
5. **Pick Date & Time** from available slots
6. **Enter reason** for visit
7. **Confirm booking**

### View Your Appointments
- Scroll to "My Appointments" section
- See all upcoming and past appointments
- Cancel pending appointments

---

## For Doctors

### Setup Your Practice

#### Add Locations (via API):
```javascript
POST /api/doctor/locations
{
    "location_name": "City Hospital",
    "address": "123 Main St",
    "city": "Colombo",
    "phone": "+94 11 234 5678"
}
```

#### Set Availability:
```javascript
POST /api/doctor/availability
{
    "location_id": 1,
    "day_of_week": 1,  // 0=Mon, 1=Tue, ..., 6=Sun
    "start_time": "09:00",
    "end_time": "17:00",
    "slot_duration": 30
}
```

---

## Database Tables

### doctor_locations
- Stores practice locations
- Multiple locations per doctor
- Address, city, phone

### doctor_availability
- Weekly schedule
- Day of week + time range
- Configurable slot duration

### appointments
- All bookings
- Patient + Doctor + Location
- Status tracking
- Reason and notes

---

## Features

### Booking Wizard
✅ 4-step process
✅ Visual progress indicator
✅ Back navigation
✅ Smooth transitions

### Location Display
✅ Full address
✅ Contact information
✅ City-wise grouping

### Time Slots
✅ 30-minute intervals
✅ Available slots only
✅ Prevents double-booking
✅ Visual selection

### Appointment Management
✅ View all appointments
✅ Status tracking
✅ Cancel option
✅ Color-coded status

---

## API Endpoints

### Patient APIs
```
GET  /api/appointments/doctors          # List all doctors
GET  /api/appointments/locations/:id    # Doctor locations
GET  /api/appointments/slots            # Available time slots
POST /api/appointments/book             # Book appointment
GET  /api/appointments/my               # My appointments
POST /api/appointments/:id/cancel       # Cancel appointment
```

### Doctor APIs
```
GET  /api/doctor/locations              # My locations
POST /api/doctor/locations              # Add location
GET  /api/doctor/availability           # My schedule
POST /api/doctor/availability           # Set availability
GET  /api/doctor/appointments           # My appointments
```

---

## Testing

### Test Complete Flow
1. Run setup script
2. Login as user
3. Go to /appointments
4. Select doctor
5. Choose location
6. Pick date/time
7. Confirm booking
8. Check "My Appointments"

### Test Double-Booking Prevention
1. Book Tuesday 10:00 AM
2. Try booking same slot
3. Should show error
4. Slot not in available list

---

## Demo Schedule

After running setup script, doctors available:
- **Tuesday:** 9 AM - 12 PM, 2 PM - 5 PM
- **Thursday:** 9 AM - 12 PM, 2 PM - 5 PM
- **Saturday:** 9 AM - 1 PM

---

## Files Created

```
src/appointments.py              # Appointment manager
templates/appointments.html      # Booking interface
data/appointments.db            # Database
setup_appointments_demo.py      # Demo data script
```

---

## Status Values

- `pending` - Newly booked
- `confirmed` - Doctor confirmed
- `completed` - Visit finished
- `cancelled` - Cancelled by patient/doctor

---

**Ready to use!** 🎉

Start at: http://localhost:5000/appointments
