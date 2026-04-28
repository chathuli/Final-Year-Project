"""
Email Notification Service
Sends appointment confirmation emails to patients using Gmail SMTP
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


# ============================================================================
# EMAIL CONFIGURATION — update these or set as environment variables
# ============================================================================
EMAIL_HOST     = os.environ.get('EMAIL_HOST',     'smtp.gmail.com')
EMAIL_PORT     = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USER     = os.environ.get('EMAIL_USER',     'chathulidaneesha@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'etqfppjkcxutrsig')
EMAIL_FROM     = os.environ.get('EMAIL_FROM',     EMAIL_USER)
EMAIL_ENABLED  = bool(EMAIL_USER and EMAIL_PASSWORD)    # auto-disable if not configured


# Day-of-week helper
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def _format_date(date_str: str) -> str:
    """Convert YYYY-MM-DD to 'Monday, 28 April 2026'"""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%A, %d %B %Y')
    except Exception:
        return date_str


def _format_time(time_str: str) -> str:
    """Convert HH:MM to '02:30 PM'"""
    try:
        dt = datetime.strptime(time_str, '%H:%M')
        return dt.strftime('%I:%M %p')
    except Exception:
        return time_str


# ============================================================================
# HTML EMAIL TEMPLATE
# ============================================================================

def _build_html(patient_name: str, appointment: dict) -> str:
    date_fmt  = _format_date(appointment.get('appointment_date', ''))
    time_fmt  = _format_time(appointment.get('appointment_time', ''))
    doctor    = appointment.get('doctor_name', 'Your Doctor')
    location  = appointment.get('location_name', '')
    address   = appointment.get('address', '')
    city      = appointment.get('city', '')
    phone     = appointment.get('phone', 'N/A')
    reason    = appointment.get('reason', 'General Consultation')
    appt_id   = appointment.get('id', 'N/A')

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Appointment Confirmation</title>
</head>
<body style="margin:0;padding:0;font-family:'Inter',Arial,sans-serif;
             background:linear-gradient(135deg,#F4F6F9 0%,#E8EDF4 100%);min-height:100vh;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#EBF4FF;border-radius:20px;
                    box-shadow:0 8px 32px rgba(26,115,232,0.15);
                    overflow:hidden;max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#1A73E8 0%,#0D9488 100%);
                     padding:40px 40px 30px;text-align:center;position:relative;">
            <div style="font-size:48px;margin-bottom:12px;">🏥</div>
            <h1 style="color:#ffffff;margin:0;font-size:26px;font-weight:800;
                       letter-spacing:-0.5px;">Appointment Confirmed!</h1>
            <p style="color:rgba(255,255,255,0.9);margin:8px 0 0;font-size:15px;">
              Breast Cancer Detection &amp; Care System
            </p>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding:32px 40px 0;">
            <p style="color:#1C2B4A;font-size:16px;margin:0 0 8px;">
              Dear <strong>{patient_name}</strong>,
            </p>
            <p style="color:#374151;font-size:15px;line-height:1.6;margin:0;">
              Your appointment has been successfully booked. Please find the details below.
            </p>
          </td>
        </tr>

        <!-- Appointment Details Card -->
        <tr>
          <td style="padding:24px 40px;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:rgba(255,255,255,0.85);border-radius:14px;
                          border:2px solid #C7DCFF;overflow:hidden;">

              <!-- Card Header -->
              <tr>
                <td colspan="2"
                    style="background:linear-gradient(135deg,#1A73E8,#0D9488);
                           padding:14px 24px;">
                  <span style="color:#fff;font-weight:700;font-size:15px;">
                    📋 Appointment Details
                  </span>
                </td>
              </tr>

              <!-- Detail rows -->
              {_detail_row('🔖', 'Appointment ID', f'#{appt_id}')}
              {_detail_row('📅', 'Date', date_fmt)}
              {_detail_row('🕐', 'Time', time_fmt)}
              {_detail_row('👨‍⚕️', 'Doctor', doctor)}
              {_detail_row('🏥', 'Location', location)}
              {_detail_row('📍', 'Address', f'{address}, {city}' if address else city)}
              {_detail_row('📞', 'Phone', phone)}
              {_detail_row('💬', 'Reason', reason)}

            </table>
          </td>
        </tr>

        <!-- Important Notice -->
        <tr>
          <td style="padding:0 40px 24px;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#FEF9C3;border:2px solid #D97706;
                          border-radius:12px;padding:16px 20px;">
              <tr>
                <td>
                  <p style="color:#854D0E;font-weight:700;margin:0 0 8px;font-size:14px;">
                    ⚠️ Important Reminders
                  </p>
                  <ul style="color:#854D0E;font-size:13px;margin:0;padding-left:18px;
                             line-height:1.8;">
                    <li>Please arrive <strong>10–15 minutes</strong> before your appointment.</li>
                    <li>Bring any previous medical reports or test results.</li>
                    <li>If you need to cancel, please do so at least <strong>24 hours</strong> in advance.</li>
                    <li>Contact the clinic directly if you have any questions.</li>
                  </ul>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- CTA Button -->
        <tr>
          <td style="padding:0 40px 32px;text-align:center;">
            <a href="http://localhost:5000/appointments"
               style="display:inline-block;background:linear-gradient(135deg,#1A73E8,#0D9488);
                      color:#ffffff;text-decoration:none;padding:14px 36px;
                      border-radius:50px;font-weight:700;font-size:15px;
                      box-shadow:0 4px 16px rgba(26,115,232,0.35);">
              View My Appointments
            </a>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#1C2B4A;padding:24px 40px;text-align:center;">
            <p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0 0 6px;">
              This is an automated message from the Breast Cancer Detection System.
            </p>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:0;">
              Please do not reply to this email.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def _detail_row(icon: str, label: str, value: str) -> str:
    """Generate a single detail row inside the appointment card."""
    return f"""
              <tr style="border-bottom:1px solid #EBF4FF;">
                <td style="padding:12px 24px;width:40%;vertical-align:top;">
                  <span style="color:#6B7280;font-size:13px;font-weight:600;">
                    {icon} {label}
                  </span>
                </td>
                <td style="padding:12px 24px;vertical-align:top;">
                  <span style="color:#1C2B4A;font-size:14px;font-weight:600;">
                    {value}
                  </span>
                </td>
              </tr>"""


def _build_plain(patient_name: str, appointment: dict) -> str:
    """Plain-text fallback."""
    date_fmt = _format_date(appointment.get('appointment_date', ''))
    time_fmt = _format_time(appointment.get('appointment_time', ''))
    return f"""
Appointment Confirmed — Breast Cancer Detection System
=======================================================

Dear {patient_name},

Your appointment has been successfully booked.

APPOINTMENT DETAILS
-------------------
Appointment ID : #{appointment.get('id', 'N/A')}
Date           : {date_fmt}
Time           : {time_fmt}
Doctor         : {appointment.get('doctor_name', 'Your Doctor')}
Location       : {appointment.get('location_name', '')}
Address        : {appointment.get('address', '')}, {appointment.get('city', '')}
Phone          : {appointment.get('phone', 'N/A')}
Reason         : {appointment.get('reason', 'General Consultation')}

REMINDERS
---------
• Arrive 10–15 minutes before your appointment.
• Bring any previous medical reports or test results.
• Cancel at least 24 hours in advance if needed.

View your appointments: http://localhost:5000/appointments

This is an automated message. Please do not reply.
"""


# ============================================================================
# LOGIN NOTIFICATION EMAIL
# ============================================================================

def _build_login_html(user_name: str, login_time: str, role: str) -> str:
    role_label = role.capitalize()
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login Notification</title>
</head>
<body style="margin:0;padding:0;font-family:'Inter',Arial,sans-serif;
             background:linear-gradient(135deg,#F4F6F9 0%,#E8EDF4 100%);min-height:100vh;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#EBF4FF;border-radius:20px;
                    box-shadow:0 8px 32px rgba(26,115,232,0.15);
                    overflow:hidden;max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#1A73E8 0%,#0D9488 100%);
                     padding:40px 40px 30px;text-align:center;">
            <div style="font-size:48px;margin-bottom:12px;">🔐</div>
            <h1 style="color:#ffffff;margin:0;font-size:26px;font-weight:800;">
              Login Notification
            </h1>
            <p style="color:rgba(255,255,255,0.9);margin:8px 0 0;font-size:15px;">
              Breast Cancer Detection &amp; Care System
            </p>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:32px 40px;">
            <p style="color:#1C2B4A;font-size:16px;margin:0 0 8px;">
              Dear <strong>{user_name}</strong>,
            </p>
            <p style="color:#374151;font-size:15px;line-height:1.6;margin:0 0 24px;">
              A successful login was recorded on your <strong>{role_label}</strong> account.
            </p>

            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:rgba(255,255,255,0.85);border-radius:14px;
                          border:2px solid #C7DCFF;overflow:hidden;">
              <tr>
                <td colspan="2"
                    style="background:linear-gradient(135deg,#1A73E8,#0D9488);
                           padding:14px 24px;">
                  <span style="color:#fff;font-weight:700;font-size:15px;">
                    🕐 Login Details
                  </span>
                </td>
              </tr>
              {_detail_row('👤', 'Account', user_name)}
              {_detail_row('🏷️', 'Role', role_label)}
              {_detail_row('📅', 'Date &amp; Time', login_time)}
            </table>

            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#FEF9C3;border:2px solid #D97706;
                          border-radius:12px;padding:16px 20px;margin-top:24px;">
              <tr>
                <td>
                  <p style="color:#854D0E;font-weight:700;margin:0 0 8px;font-size:14px;">
                    ⚠️ Security Notice
                  </p>
                  <p style="color:#854D0E;font-size:13px;margin:0;line-height:1.7;">
                    If this was not you, please contact the system administrator immediately
                    and change your password.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#1C2B4A;padding:24px 40px;text-align:center;">
            <p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0 0 6px;">
              This is an automated security notification from the Breast Cancer Detection System.
            </p>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:0;">
              Please do not reply to this email.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def send_login_notification(user_email: str, user_name: str, role: str = 'user') -> dict:
    """
    Send a login notification email to the user.

    Parameters
    ----------
    user_email  : recipient email address
    user_name   : user's full name or username
    role        : user role ('user', 'doctor', 'admin')

    Returns
    -------
    {'success': True}  or  {'success': False, 'error': '...'}
    """
    if not EMAIL_ENABLED:
        print(f"[EMAIL] Login notification skipped (not configured) for: {user_email}")
        return {'success': False, 'error': 'Email service not configured'}

    try:
        login_time = datetime.now().strftime('%A, %d %B %Y at %I:%M %p')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 Login Notification — Breast Cancer Detection System'
        msg['From']    = f"Breast Cancer Detection System <{EMAIL_FROM}>"
        msg['To']      = user_email

        plain = (
            f"Login Notification\n\n"
            f"Dear {user_name},\n\n"
            f"A successful login was recorded on your {role.capitalize()} account.\n\n"
            f"Date & Time : {login_time}\n"
            f"Role        : {role.capitalize()}\n\n"
            f"If this was not you, please contact the administrator immediately.\n\n"
            f"This is an automated message. Please do not reply."
        )

        msg.attach(MIMEText(plain, 'plain', 'utf-8'))
        msg.attach(MIMEText(_build_login_html(user_name, login_time, role), 'html', 'utf-8'))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, [user_email], msg.as_string())

        print(f"[EMAIL] Login notification sent to {user_email}")
        return {'success': True}

    except smtplib.SMTPAuthenticationError:
        msg = 'SMTP authentication failed. Check EMAIL_USER / EMAIL_PASSWORD.'
        print(f"[EMAIL ERROR] {msg}")
        return {'success': False, 'error': msg}

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return {'success': False, 'error': str(e)}


# ============================================================================
# DOCTOR APPOINTMENT CONFIRMATION EMAIL
# ============================================================================

def _build_confirmed_html(patient_name: str, appointment: dict, doctor_notes: str = '') -> str:
    date_fmt  = _format_date(appointment.get('appointment_date', ''))
    time_fmt  = _format_time(appointment.get('appointment_time', ''))
    doctor    = appointment.get('doctor_name', 'Your Doctor')
    location  = appointment.get('location_name', '')
    address   = appointment.get('address', '')
    city      = appointment.get('city', '')
    phone     = appointment.get('phone', 'N/A')
    reason    = appointment.get('reason', 'General Consultation')
    appt_id   = appointment.get('id', 'N/A')

    notes_section = ''
    if doctor_notes:
        notes_section = f"""
        <tr>
          <td style="padding:0 40px 24px;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#F0FDF4;border:2px solid #16A34A;
                          border-radius:12px;padding:16px 20px;">
              <tr>
                <td>
                  <p style="color:#15803D;font-weight:700;margin:0 0 8px;font-size:14px;">
                    💬 Doctor's Notes
                  </p>
                  <p style="color:#15803D;font-size:13px;margin:0;line-height:1.7;">
                    {doctor_notes}
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>"""

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Appointment Confirmed by Doctor</title>
</head>
<body style="margin:0;padding:0;font-family:'Inter',Arial,sans-serif;
             background:linear-gradient(135deg,#F4F6F9 0%,#E8EDF4 100%);min-height:100vh;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#EBF4FF;border-radius:20px;
                    box-shadow:0 8px 32px rgba(26,115,232,0.15);
                    overflow:hidden;max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#16A34A 0%,#0D9488 100%);
                     padding:40px 40px 30px;text-align:center;">
            <div style="font-size:48px;margin-bottom:12px;">✅</div>
            <h1 style="color:#ffffff;margin:0;font-size:26px;font-weight:800;">
              Doctor Confirmed Your Appointment!
            </h1>
            <p style="color:rgba(255,255,255,0.9);margin:8px 0 0;font-size:15px;">
              Breast Cancer Detection &amp; Care System
            </p>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding:32px 40px 0;">
            <p style="color:#1C2B4A;font-size:16px;margin:0 0 8px;">
              Dear <strong>{patient_name}</strong>,
            </p>
            <p style="color:#374151;font-size:15px;line-height:1.6;margin:0;">
              Great news! <strong>Dr. {doctor}</strong> has confirmed your appointment.
              Please see the details below.
            </p>
          </td>
        </tr>

        <!-- Appointment Details Card -->
        <tr>
          <td style="padding:24px 40px;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:rgba(255,255,255,0.85);border-radius:14px;
                          border:2px solid #BBF7D0;overflow:hidden;">
              <tr>
                <td colspan="2"
                    style="background:linear-gradient(135deg,#16A34A,#0D9488);
                           padding:14px 24px;">
                  <span style="color:#fff;font-weight:700;font-size:15px;">
                    📋 Confirmed Appointment Details
                  </span>
                </td>
              </tr>
              {_detail_row('🔖', 'Appointment ID', f'#{appt_id}')}
              {_detail_row('📅', 'Date', date_fmt)}
              {_detail_row('🕐', 'Time', time_fmt)}
              {_detail_row('👨‍⚕️', 'Doctor', doctor)}
              {_detail_row('🏥', 'Location', location)}
              {_detail_row('📍', 'Address', f'{address}, {city}' if address else city)}
              {_detail_row('📞', 'Phone', phone)}
              {_detail_row('💬', 'Reason', reason)}
            </table>
          </td>
        </tr>

        {notes_section}

        <!-- Reminders -->
        <tr>
          <td style="padding:0 40px 24px;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#FEF9C3;border:2px solid #D97706;
                          border-radius:12px;padding:16px 20px;">
              <tr>
                <td>
                  <p style="color:#854D0E;font-weight:700;margin:0 0 8px;font-size:14px;">
                    ⚠️ Important Reminders
                  </p>
                  <ul style="color:#854D0E;font-size:13px;margin:0;padding-left:18px;
                             line-height:1.8;">
                    <li>Please arrive <strong>10–15 minutes</strong> before your appointment.</li>
                    <li>Bring any previous medical reports or test results.</li>
                    <li>If you need to cancel, please do so at least <strong>24 hours</strong> in advance.</li>
                    <li>Contact the clinic directly if you have any questions.</li>
                  </ul>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- CTA -->
        <tr>
          <td style="padding:0 40px 32px;text-align:center;">
            <a href="http://localhost:5000/appointments"
               style="display:inline-block;background:linear-gradient(135deg,#16A34A,#0D9488);
                      color:#ffffff;text-decoration:none;padding:14px 36px;
                      border-radius:50px;font-weight:700;font-size:15px;
                      box-shadow:0 4px 16px rgba(22,163,74,0.35);">
              View My Appointments
            </a>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#1C2B4A;padding:24px 40px;text-align:center;">
            <p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0 0 6px;">
              This is an automated message from the Breast Cancer Detection System.
            </p>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:0;">
              Please do not reply to this email.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def send_appointment_confirmed_by_doctor(patient_email: str, patient_name: str,
                                          appointment: dict,
                                          doctor_notes: str = '') -> dict:
    """
    Send an email to the patient when a doctor confirms their appointment.

    Parameters
    ----------
    patient_email   : patient's email address
    patient_name    : patient's full name
    appointment     : appointment dict (same shape as send_appointment_confirmation)
    doctor_notes    : optional notes added by the doctor

    Returns
    -------
    {'success': True}  or  {'success': False, 'error': '...'}
    """
    if not EMAIL_ENABLED:
        print(f"[EMAIL] Doctor-confirmation email skipped (not configured) for: {patient_email}")
        return {'success': False, 'error': 'Email service not configured'}

    try:
        date_fmt = _format_date(appointment.get('appointment_date', ''))
        time_fmt = _format_time(appointment.get('appointment_time', ''))
        doctor   = appointment.get('doctor_name', 'Your Doctor')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = (
            f"✅ Appointment Confirmed by Dr. {doctor} — "
            f"{date_fmt} at {time_fmt}"
        )
        msg['From'] = f"Breast Cancer Detection System <{EMAIL_FROM}>"
        msg['To']   = patient_email

        plain = (
            f"Appointment Confirmed by Doctor\n\n"
            f"Dear {patient_name},\n\n"
            f"Dr. {doctor} has confirmed your appointment.\n\n"
            f"Date    : {date_fmt}\n"
            f"Time    : {time_fmt}\n"
            f"Doctor  : {doctor}\n"
            f"Location: {appointment.get('location_name', '')}\n"
            f"Reason  : {appointment.get('reason', 'General Consultation')}\n"
        )
        if doctor_notes:
            plain += f"\nDoctor's Notes: {doctor_notes}\n"
        plain += (
            "\nPlease arrive 10-15 minutes early and bring any previous reports.\n\n"
            "View appointments: http://localhost:5000/appointments\n\n"
            "This is an automated message. Please do not reply."
        )

        msg.attach(MIMEText(plain, 'plain', 'utf-8'))
        msg.attach(MIMEText(
            _build_confirmed_html(patient_name, appointment, doctor_notes),
            'html', 'utf-8'
        ))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, [patient_email], msg.as_string())

        print(f"[EMAIL] Doctor-confirmation email sent to {patient_email}")
        return {'success': True}

    except smtplib.SMTPAuthenticationError:
        msg = 'SMTP authentication failed. Check EMAIL_USER / EMAIL_PASSWORD.'
        print(f"[EMAIL ERROR] {msg}")
        return {'success': False, 'error': msg}

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return {'success': False, 'error': str(e)}


# ============================================================================
# PUBLIC API
# ============================================================================

def send_appointment_confirmation(patient_email: str, patient_name: str,
                                   appointment: dict) -> dict:
    """
    Send an appointment confirmation email.

    Parameters
    ----------
    patient_email   : recipient email address
    patient_name    : patient's full name
    appointment     : dict with keys:
                        id, appointment_date, appointment_time,
                        doctor_name, location_name, address, city,
                        phone, reason

    Returns
    -------
    {'success': True}  or  {'success': False, 'error': '...'}
    """
    if not EMAIL_ENABLED:
        print("[EMAIL] Email not configured — skipping confirmation email.")
        print(f"[EMAIL] Would have sent to: {patient_email}")
        return {'success': False, 'error': 'Email service not configured'}

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = (
            f"✅ Appointment Confirmed — "
            f"{_format_date(appointment.get('appointment_date', ''))} "
            f"at {_format_time(appointment.get('appointment_time', ''))}"
        )
        msg['From']    = f"Breast Cancer Detection System <{EMAIL_FROM}>"
        msg['To']      = patient_email

        plain_part = MIMEText(_build_plain(patient_name, appointment), 'plain', 'utf-8')
        html_part  = MIMEText(_build_html(patient_name, appointment),  'html',  'utf-8')

        msg.attach(plain_part)   # plain first, HTML preferred by clients
        msg.attach(html_part)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, [patient_email], msg.as_string())

        print(f"[EMAIL] Confirmation sent to {patient_email}")
        return {'success': True}

    except smtplib.SMTPAuthenticationError:
        msg = 'SMTP authentication failed. Check EMAIL_USER / EMAIL_PASSWORD.'
        print(f"[EMAIL ERROR] {msg}")
        return {'success': False, 'error': msg}

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return {'success': False, 'error': str(e)}
