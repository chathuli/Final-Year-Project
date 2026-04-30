# Application Run කරන්නේ කෙසේද

## Method 1: Command Line (Recommended)

### Windows:

1. **Terminal එකක් open කරන්න** (PowerShell හෝ CMD)

2. **Project directory එකට යන්න:**
   ```bash
   cd "D:\Yr3 Sem1\Final Year Project-B"
   ```

3. **Virtual environment activate කරන්න:**
   ```bash
   venv\Scripts\activate
   ```

4. **Application එක run කරන්න:**
   ```bash
   python src/app.py
   ```

5. **Browser එකේ open කරන්න:**
   ```
   http://localhost:5000
   ```

## Method 2: Using Batch File

1. **Double-click කරන්න:** `start_server.bat`

2. **Browser එකේ open කරන්න:**
   ```
   http://localhost:5000
   ```

## Method 3: VS Code Terminal

1. **VS Code එකේ Terminal open කරන්න:** `Ctrl + ` (backtick)

2. **Run කරන්න:**
   ```bash
   python src/app.py
   ```

3. **Browser එකේ open කරන්න:**
   ```
   http://localhost:5000
   ```

## ✅ Server Running වෙනවාද Check කරන්න:

Terminal එකේ මෙහෙම පෙන්වන්න ඕන:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

## 🌐 Access කරන්න:

### Main Pages:
- **Home:** http://localhost:5000/
- **Login:** http://localhost:5000/login
- **History:** http://localhost:5000/history
- **Dashboard:** http://localhost:5000/dashboard
- **Symptom Input:** http://localhost:5000/ (home page)

### Test Accounts:

#### Admin:
- Username: `admin`
- Password: `admin123`

#### Doctor:
- Username: `doctor`
- Password: `doctor123`

#### Regular User:
- Register new account හෝ existing account use කරන්න

## 🛑 Server Stop කරන්න:

Terminal එකේ:
```
Ctrl + C
```

## ⚠️ Common Issues:

### Issue 1: Port Already in Use
```
Error: Address already in use
```

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue 2: Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Issue 3: Database Error
```
Error: database is locked
```

**Solution:**
```bash
# Close any programs accessing the database
# Restart the server
```

## 📊 Test the New Features:

### 1. Test Symptom Analysis:
1. Go to Home page
2. Fill in symptom form
3. Submit
4. Go to History page
5. Check for 🩺 Symptom Analysis entry
6. Click "👁️ View Details"
7. Verify modal shows complete symptom data

### 2. Test Report Generation:
1. Go to History page
2. Click "📄 Report" button
3. Verify PDF downloads
4. Open PDF and check:
   - For symptom predictions: Should show symptom report
   - For manual predictions: Should show patient/technical report

### 3. Test Delete Function (Admin only):
1. Login as admin
2. Go to History page
3. Verify Delete column shows 🗑️ Delete button
4. Click delete on a test prediction
5. Confirm deletion works

## 🔄 After Making Changes:

1. **Stop server:** `Ctrl + C`
2. **Restart server:** `python src/app.py`
3. **Clear browser cache:** `Ctrl + Shift + Delete`
4. **Hard refresh:** `Ctrl + F5`

## 📝 Development Mode:

Server එක debug mode එකේ run වෙනවා, එනම්:
- Code changes automatically detect වෙනවා
- Server auto-restart වෙනවා
- Detailed error messages පෙන්වනවා

## 🎯 Quick Start:

```bash
# One-line command to start everything:
cd "D:\Yr3 Sem1\Final Year Project-B" && venv\Scripts\activate && python src/app.py
```

Then open: http://localhost:5000

---

**Happy Testing! 🎉**

If you encounter any issues, check the terminal output for error messages.
