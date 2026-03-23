"""
Appointment Management System
Handles doctor appointments, schedules, and locations
"""

import sqlite3
import os
from datetime import datetime, timedelta

class AppointmentManager:
    """Manages doctor appointments and availability"""
    
    def __init__(self, db_path='data/appointments.db'):
        """Initialize appointment manager"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize appointments database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Doctor locations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                location_name TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                phone TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (doctor_id) REFERENCES users(id)
            )
        ''')
        
        # Doctor availability/schedule table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                location_id INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                slot_duration INTEGER DEFAULT 30,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (doctor_id) REFERENCES users(id),
                FOREIGN KEY (location_id) REFERENCES doctor_locations(id)
            )
        ''')
        
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                location_id INTEGER NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TEXT NOT NULL,
                duration INTEGER DEFAULT 30,
                status TEXT DEFAULT 'pending',
                reason TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES users(id),
                FOREIGN KEY (doctor_id) REFERENCES users(id),
                FOREIGN KEY (location_id) REFERENCES doctor_locations(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Appointments database initialized")
    
    # ============================================================================
    # LOCATION MANAGEMENT
    # ============================================================================
    
    def add_location(self, doctor_id, location_name, address, city, phone=None):
        """Add a location for a doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO doctor_locations (doctor_id, location_name, address, city, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (doctor_id, location_name, address, city, phone))
            
            location_id = cursor.lastrowid
            conn.commit()
            
            return {
                'success': True,
                'location_id': location_id,
                'message': 'Location added successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def get_doctor_locations(self, doctor_id):
        """Get all locations for a doctor"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM doctor_locations 
            WHERE doctor_id = ? AND is_active = 1
            ORDER BY location_name
        ''', (doctor_id,))
        
        locations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return locations
    
    def get_all_locations(self):
        """Get all active locations with doctor info"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                dl.*,
                u.full_name as doctor_name,
                u.email as doctor_email
            FROM doctor_locations dl
            JOIN users u ON dl.doctor_id = u.id
            WHERE dl.is_active = 1 AND u.role = 'doctor'
            ORDER BY dl.city, dl.location_name
        ''')
        
        locations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return locations
    
    # ============================================================================
    # AVAILABILITY MANAGEMENT
    # ============================================================================
    
    def add_availability(self, doctor_id, location_id, day_of_week, start_time, end_time, slot_duration=30):
        """Add doctor availability schedule"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO doctor_availability 
                (doctor_id, location_id, day_of_week, start_time, end_time, slot_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (doctor_id, location_id, day_of_week, start_time, end_time, slot_duration))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'Availability added successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def get_doctor_availability(self, doctor_id, location_id=None):
        """Get doctor's availability schedule"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if location_id:
            cursor.execute('''
                SELECT da.*, dl.location_name, dl.address, dl.city
                FROM doctor_availability da
                JOIN doctor_locations dl ON da.location_id = dl.id
                WHERE da.doctor_id = ? AND da.location_id = ? AND da.is_active = 1
                ORDER BY da.day_of_week, da.start_time
            ''', (doctor_id, location_id))
        else:
            cursor.execute('''
                SELECT da.*, dl.location_name, dl.address, dl.city
                FROM doctor_availability da
                JOIN doctor_locations dl ON da.location_id = dl.id
                WHERE da.doctor_id = ? AND da.is_active = 1
                ORDER BY da.day_of_week, da.start_time
            ''', (doctor_id,))
        
        availability = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return availability
    
    def get_available_slots(self, doctor_id, location_id, date):
        """Get available time slots for a specific date"""
        # Get day of week (0 = Monday, 6 = Sunday)
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        day_of_week = date_obj.weekday()
        
        # Get doctor's schedule for this day
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM doctor_availability
            WHERE doctor_id = ? AND location_id = ? AND day_of_week = ? AND is_active = 1
        ''', (doctor_id, location_id, day_of_week))
        
        schedules = cursor.fetchall()
        
        if not schedules:
            conn.close()
            return []
        
        # Get existing appointments for this date
        cursor.execute('''
            SELECT appointment_time, duration FROM appointments
            WHERE doctor_id = ? AND location_id = ? AND appointment_date = ?
            AND status != 'cancelled'
        ''', (doctor_id, location_id, date))
        
        booked_slots = cursor.fetchall()
        conn.close()
        
        # Generate available slots
        available_slots = []
        
        for schedule in schedules:
            start_time = schedule['start_time']
            end_time = schedule['end_time']
            slot_duration = schedule['slot_duration']
            
            # Generate time slots
            current_time = datetime.strptime(start_time, '%H:%M')
            end_datetime = datetime.strptime(end_time, '%H:%M')
            
            while current_time < end_datetime:
                time_str = current_time.strftime('%H:%M')
                
                # Check if slot is already booked
                is_booked = False
                for booked in booked_slots:
                    if booked['appointment_time'] == time_str:
                        is_booked = True
                        break
                
                if not is_booked:
                    available_slots.append({
                        'time': time_str,
                        'display': current_time.strftime('%I:%M %p')
                    })
                
                current_time += timedelta(minutes=slot_duration)
        
        return available_slots
    
    # ============================================================================
    # APPOINTMENT MANAGEMENT
    # ============================================================================
    
    def book_appointment(self, patient_id, doctor_id, location_id, appointment_date, 
                        appointment_time, reason=None, notes=None):
        """Book an appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if slot is available
            cursor.execute('''
                SELECT id FROM appointments
                WHERE doctor_id = ? AND location_id = ? 
                AND appointment_date = ? AND appointment_time = ?
                AND status != 'cancelled'
            ''', (doctor_id, location_id, appointment_date, appointment_time))
            
            if cursor.fetchone():
                return {
                    'success': False,
                    'error': 'This time slot is already booked'
                }
            
            # Book appointment
            cursor.execute('''
                INSERT INTO appointments 
                (patient_id, doctor_id, location_id, appointment_date, appointment_time, reason, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, doctor_id, location_id, appointment_date, appointment_time, reason, notes))
            
            appointment_id = cursor.lastrowid
            conn.commit()
            
            return {
                'success': True,
                'appointment_id': appointment_id,
                'message': 'Appointment booked successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def get_patient_appointments(self, patient_id, status=None):
        """Get all appointments for a patient"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT 
                    a.*,
                    u.full_name as doctor_name,
                    u.email as doctor_email,
                    dl.location_name,
                    dl.address,
                    dl.city,
                    dl.phone
                FROM appointments a
                JOIN users u ON a.doctor_id = u.id
                JOIN doctor_locations dl ON a.location_id = dl.id
                WHERE a.patient_id = ? AND a.status = ?
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            ''', (patient_id, status))
        else:
            cursor.execute('''
                SELECT 
                    a.*,
                    u.full_name as doctor_name,
                    u.email as doctor_email,
                    dl.location_name,
                    dl.address,
                    dl.city,
                    dl.phone
                FROM appointments a
                JOIN users u ON a.doctor_id = u.id
                JOIN doctor_locations dl ON a.location_id = dl.id
                WHERE a.patient_id = ?
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            ''', (patient_id,))
        
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return appointments
    
    def get_doctor_appointments(self, doctor_id, date=None, status=None):
        """Get all appointments for a doctor"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                a.*,
                u.full_name as patient_name,
                u.email as patient_email,
                dl.location_name,
                dl.address,
                dl.city
            FROM appointments a
            JOIN users u ON a.patient_id = u.id
            JOIN doctor_locations dl ON a.location_id = dl.id
            WHERE a.doctor_id = ?
        '''
        params = [doctor_id]
        
        if date:
            query += ' AND a.appointment_date = ?'
            params.append(date)
        
        if status:
            query += ' AND a.status = ?'
            params.append(status)
        
        query += ' ORDER BY a.appointment_date, a.appointment_time'
        
        cursor.execute(query, params)
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return appointments
    
    def update_appointment_status(self, appointment_id, status, notes=None):
        """Update appointment status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if notes:
                cursor.execute('''
                    UPDATE appointments 
                    SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, notes, appointment_id))
            else:
                cursor.execute('''
                    UPDATE appointments 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, appointment_id))
            
            conn.commit()
            
            return {
                'success': True,
                'message': f'Appointment {status} successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def cancel_appointment(self, appointment_id, user_id):
        """Cancel an appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verify user owns this appointment
            cursor.execute('''
                SELECT patient_id, doctor_id FROM appointments WHERE id = ?
            ''', (appointment_id,))
            
            result = cursor.fetchone()
            if not result:
                return {'success': False, 'error': 'Appointment not found'}
            
            patient_id, doctor_id = result
            
            if user_id not in [patient_id, doctor_id]:
                return {'success': False, 'error': 'Unauthorized'}
            
            # Cancel appointment
            cursor.execute('''
                UPDATE appointments 
                SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (appointment_id,))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'Appointment cancelled successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def get_all_doctors(self):
        """Get all doctors with their locations"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                u.id,
                u.full_name,
                u.email,
                COUNT(DISTINCT dl.id) as location_count
            FROM users u
            LEFT JOIN doctor_locations dl ON u.id = dl.doctor_id AND dl.is_active = 1
            WHERE u.role = 'doctor' AND u.is_active = 1
            GROUP BY u.id
            ORDER BY u.full_name
        ''')
        
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return doctors
