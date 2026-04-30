# Security Fixes Applied

This document outlines the critical security issues that have been fixed in the system.

## Issues Fixed

### 1. ✅ Hardcoded Credentials Removed
**Issue:** Gmail credentials were hardcoded in `config.py`  
**Fix:** Moved to environment variables
- `EMAIL_USER` and `EMAIL_PASSWORD` now loaded from environment
- Created `.env.template` for configuration
- Added `.env` to `.gitignore`

**Action Required:**
```bash
# Copy template and fill in your credentials
cp .env.template .env
# Edit .env and add your actual credentials
```

### 2. ✅ Upgraded Password Hashing
**Issue:** Passwords hashed with SHA-256 (vulnerable to brute-force)  
**Fix:** Upgraded to bcrypt
- Implemented `bcrypt` for secure password hashing
- Added `verify_password()` method for authentication
- Migration script converts existing passwords

**Action Required:**
```bash
# Install bcrypt
pip install bcrypt

# Run migration script
python migrate_security_fixes.py
```

### 3. ✅ User Data Isolation
**Issue:** No `user_id` in predictions table - all users could see all predictions  
**Fix:** Added user-based data isolation
- Added `user_id` foreign key to predictions table
- All prediction queries now filtered by user
- Admin users can see all predictions
- Regular users only see their own data

**Action Required:**
```bash
# Run migration script to add user_id column
python migrate_security_fixes.py
```

### 4. ✅ Rate Limiting Added
**Issue:** No protection against automated attacks  
**Fix:** Implemented Flask-Limiter
- Login: 10 attempts per minute
- Registration: 5 attempts per hour
- Global: 200 requests per day, 50 per hour

**Action Required:**
```bash
# Install Flask-Limiter
pip install Flask-Limiter
```

### 5. ✅ API Routes Protected
**Issue:** `/api/history` and `/api/statistics` were unauthenticated  
**Fix:** Added `@login_required` decorator
- All API routes now require authentication
- User data properly isolated

### 6. ✅ Medical Disclaimer Added
**Issue:** No clinical context for AI results  
**Fix:** Added prominent medical disclaimers
- Disclaimer on symptom checker page
- Disclaimer on advanced analysis page
- Clear statement: "For educational/screening purposes only"
- Emphasizes need for professional medical diagnosis

## Installation & Migration

### Step 1: Install New Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variables
```bash
# Windows
set EMAIL_USER=your-email@gmail.com
set EMAIL_PASSWORD=your-app-password

# Linux/Mac
export EMAIL_USER=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
```

Or create a `.env` file:
```bash
cp .env.template .env
# Edit .env with your credentials
```

### Step 3: Run Migration Script
```bash
python migrate_security_fixes.py
```

This will:
- Add `user_id` column to predictions table
- Convert all passwords from SHA-256 to bcrypt
- Create `.env.template` file
- Update `.gitignore`

### Step 4: Restart Application
```bash
# Stop any running instances
taskkill /F /IM python.exe

# Start the application
python src/app.py
```

### Step 5: Reset User Passwords
After migration, users will have temporary passwords:
- Admin: `admin123` (default)
- Other users: `temp{user_id}123` (e.g., `temp2123`)

**All users should change their passwords immediately after migration.**

## Security Best Practices

### For Deployment:
1. **Never commit `.env` file** - it contains secrets
2. **Use strong SECRET_KEY** - generate with `secrets.token_hex(32)`
3. **Enable HTTPS** - use SSL/TLS certificates
4. **Regular backups** - backup databases regularly
5. **Monitor logs** - watch for suspicious activity
6. **Update dependencies** - keep packages up to date
7. **Limit admin access** - only trusted personnel

### For Development:
1. **Use separate databases** - dev vs production
2. **Test credentials** - use test accounts, not real ones
3. **Code review** - review security changes
4. **Penetration testing** - test for vulnerabilities

## Verification Checklist

- [ ] Installed bcrypt and Flask-Limiter
- [ ] Set EMAIL_USER and EMAIL_PASSWORD environment variables
- [ ] Ran migration script successfully
- [ ] Verified predictions table has user_id column
- [ ] Tested login with bcrypt passwords
- [ ] Confirmed rate limiting works (try multiple failed logins)
- [ ] Verified users can only see their own predictions
- [ ] Confirmed medical disclaimer appears on result pages
- [ ] Removed hardcoded credentials from config.py
- [ ] Added .env to .gitignore
- [ ] All users changed their passwords

## Support

If you encounter issues during migration:
1. Check Python version (3.8+)
2. Verify all dependencies installed
3. Check database file permissions
4. Review error messages in console
5. Backup databases before migration

## Additional Recommendations

### Future Enhancements:
1. **CSRF Protection** - Add Flask-WTF for CSRF tokens
2. **Session Security** - Implement secure session management
3. **Input Validation** - Add comprehensive input sanitization
4. **Audit Logging** - Log all security-relevant events
5. **2FA** - Implement two-factor authentication
6. **Password Policy** - Enforce strong password requirements
7. **Account Lockout** - Lock accounts after failed attempts
8. **Security Headers** - Add security headers (CSP, HSTS, etc.)

---

**Last Updated:** 2026-04-30  
**Version:** 1.0.0
