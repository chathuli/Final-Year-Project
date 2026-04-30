# Changes පෙන්වන්න Instructions

## Problem
Browser cache එක නිසා changes පෙන්වෙන්නේ නැහැ.

## Solution - මේ steps follow කරන්න:

### Step 1: Server එක Stop කරන්න
```bash
# Terminal එකේ Ctrl+C press කරන්න
# හෝ terminal එක close කරන්න
```

### Step 2: Browser Cache Clear කරන්න

#### Chrome/Edge:
1. `Ctrl + Shift + Delete` press කරන්න
2. "Cached images and files" select කරන්න
3. "Clear data" click කරන්න

#### හෝ Hard Refresh:
1. History page එක open කරන්න
2. `Ctrl + F5` press කරන්න (Windows)
3. හෝ `Ctrl + Shift + R` press කරන්න

### Step 3: Server එක Restart කරන්න
```bash
# Terminal එකේ:
cd path/to/your/project
python src/app.py
```

### Step 4: Browser එක Refresh කරන්න
1. Browser එක close කරන්න
2. Browser එක ආපහු open කරන්න
3. `http://localhost:5000/history` යන්න
4. Login කරන්න
5. History page එක check කරන්න

## Quick Test කරන්න:

### Terminal එකේ run කරන්න:
```bash
# Check if changes are in the files
python -c "import src.app as app; print('Report generation updated!' if 'symptom' in open('src/app.py').read() else 'Not updated')"
```

## Changes තියෙන Files:

1. **src/app.py** - Line 279-350 (generate_report function)
2. **src/report_generator.py** - End of file (_generate_symptom_report method)
3. **templates/history.html** - Table structure (lines 160-230)

## Verify Changes:

### Check src/app.py:
```bash
# Terminal එකේ:
grep -n "prediction_type.*symptom" src/app.py
```
Output එකේ line numbers පෙන්වන්න ඕන.

### Check report_generator.py:
```bash
# Terminal එකේ:
grep -n "_generate_symptom_report" src/report_generator.py
```
Output එකේ method එක තියෙනවා කියලා පෙන්වන්න ඕන.

### Check history.html:
```bash
# Terminal එකේ:
grep -n "Delete" templates/history.html | head -5
```
Delete column එක තියෙනවා කියලා පෙන්වන්න ඕන.

## Still Not Working?

### Option 1: Force Reload
1. Browser DevTools open කරන්න (F12)
2. Network tab එකට යන්න
3. "Disable cache" checkbox එක tick කරන්න
4. Page එක reload කරන්න

### Option 2: Incognito Mode
1. Incognito/Private window එකක් open කරන්න
2. Application එකට login කරන්න
3. History page එක check කරන්න

### Option 3: Different Browser
1. වෙනත් browser එකක් use කරන්න
2. Application එකට login කරන්න
3. History page එක check කරන්න

## Expected Result:

History page එකේ table එක මෙහෙම පෙන්වන්න ඕන:

```
╔════╦═══════════════╦═══════════════════╦════════════╦════════════╦═══════════╦════════╗
║ ID ║ Date & Time   ║ Type              ║ Confidence ║ Risk Level ║ Actions   ║ Delete ║
╠════╬═══════════════╬═══════════════════╬════════════╬════════════╬═══════════╬════════╣
║ 52 ║ 4/29/26 2:18  ║ 🩺 Symptom        ║ 85.0%      ║ Moderate   ║ 👁️ | 📄   ║ 🗑️     ║
╚════╩═══════════════╩═══════════════════╩════════════╩════════════╩═══════════╩════════╝
```

## Debug කරන්න:

### Browser Console Check:
1. F12 press කරන්න
2. Console tab එකට යන්න
3. Errors තියෙනවාද බලන්න
4. Screenshot එකක් ගන්න

### Server Logs Check:
1. Terminal එක බලන්න
2. Errors print වෙනවාද බලන්න
3. Request logs බලන්න

## Contact for Help:

Changes තවමත් පෙන්වෙන්නේ නැත්නම්:
1. Browser console screenshot එකක් ගන්න
2. Server terminal output එක copy කරන්න
3. History page එකේ screenshot එකක් ගන්න
4. මට පෙන්වන්න

---

**Important:** Server restart කරලා browser cache clear කිරීම ඉතාම වැදගත්!
