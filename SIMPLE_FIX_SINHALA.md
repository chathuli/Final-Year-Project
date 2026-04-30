# Password Change Fix - සරල උපදෙස්

## ⚠️ මොකද වුනේ?

Password change feature එක වැඩ කරන්නේ නැහැ කියලා error එකක් පෙන්වනවා. මේක වෙන්නේ server එක restart කරලා නැති නිසා.

## ✅ විසඳුම - 3 Steps

### Step 1: සියලුම Python Processes Kill කරන්න

**Windows Task Manager use කරන්න:**

1. `Ctrl + Shift + Esc` press කරන්න (Task Manager open වෙනවා)
2. "Details" tab එකට යන්න
3. "python.exe" හොයන්න
4. සියලුම "python.exe" processes select කරන්න
5. "End Task" click කරන්න
6. Task Manager close කරන්න

**හෝ Command Line use කරන්න:**

```bash
taskkill /F /IM python.exe /T
```

### Step 2: Server එක Start කරන්න

**New Terminal එකක්:**

1. PowerShell හෝ CMD open කරන්න
2. Project folder එකට යන්න:
   ```bash
   cd "D:\Yr3 Sem1\Final Year Project-B"
   ```
3. Virtual environment activate කරන්න:
   ```bash
   venv\Scripts\activate
   ```
4. Server start කරන්න:
   ```bash
   python src/app.py
   ```

**හෝ Batch File use කරන්න:**

Double-click කරන්න: `FORCE_RESTART.bat`

### Step 3: Test කරන්න

1. Browser එක open කරන්න
2. යන්න: `http://localhost:5000`
3. Login කරන්න:
   - **Username:** `Amaraweera`
   - **Password:** `password123`
4. Profile page එකට යන්න
5. Password change try කරන්න
6. දැන් වැඩ කරන්න ඕන! ✅

## 🔐 Login Credentials

### ඔබේ Account:
- **Username:** `Amaraweera`
- **Password:** `password123`

### Admin Account:
- **Username:** `admin`
- **Password:** `admin123`

### Doctor Account:
- **Username:** `osandi`
- **Password:** `doctor123`

## ❓ තවමත් වැඩ කරන්නේ නැද්ද?

### Check 1: Server Running වෙනවාද?

Terminal එකේ මෙහෙම පෙන්වන්න ඕන:
```
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
```

### Check 2: Browser Cache Clear කරන්න

1. `Ctrl + Shift + Delete` press කරන්න
2. "Cached images and files" select කරන්න
3. "Clear data" click කරන්න
4. Browser close කරලා ආපහු open කරන්න

### Check 3: Incognito Mode Try කරන්න

1. `Ctrl + Shift + N` (Chrome) හෝ `Ctrl + Shift + P` (Firefox)
2. `http://localhost:5000` යන්න
3. Login කරලා test කරන්න

## 📝 මොකද Fix කළේ?

**File:** `src/app.py`
**Line:** 104

Password change කරන්න API endpoint එකක් add කරා:
- `/api/profile/change-password`

මේක:
- ✅ Current password verify කරනවා
- ✅ New password validate කරනවා
- ✅ Database එකේ update කරනවා
- ✅ Proper error messages දෙනවා

## 🎯 Quick Summary

1. **Kill Python:** Task Manager use කරලා හෝ `taskkill /F /IM python.exe /T`
2. **Start Server:** `python src/app.py`
3. **Login:** Username: `Amaraweera`, Password: `password123`
4. **Test:** Profile page එකේ password change try කරන්න

---

**දැන් වැඩ කරන්න ඕන!** 🎉

ප්‍රශ්න තියෙනවා නම්, මේ files බලන්න:
- `PASSWORD_CHANGE_FIX.md` - Technical details
- `FORCE_RESTART.bat` - Auto restart script
