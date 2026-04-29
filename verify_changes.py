"""
Verify that all changes have been applied correctly
"""

import os

print("=" * 80)
print("VERIFYING CHANGES")
print("=" * 80)

# Check 1: src/app.py
print("\n1. Checking src/app.py...")
with open('src/app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()
    
    checks = [
        ('isinstance(all_models, dict)', 'Float object error fix'),
        ("prediction_type='symptom'", 'Symptom report type'),
        ("'symptoms_data':", 'Symptoms data passing'),
        ("'prediction_type':", 'Prediction type passing')
    ]
    
    for check_str, description in checks:
        if check_str in app_content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND!")

# Check 2: src/report_generator.py
print("\n2. Checking src/report_generator.py...")
with open('src/report_generator.py', 'r', encoding='utf-8') as f:
    report_content = f.read()
    
    checks = [
        ('def _generate_symptom_report', 'Symptom report method'),
        ('Symptom-Based Breast Cancer Screening Report', 'Symptom report title'),
        ('Reported Symptoms Summary', 'Symptoms section'),
        ('Risk Assessment', 'Risk assessment section')
    ]
    
    for check_str, description in checks:
        if check_str in report_content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND!")

# Check 3: templates/history.html
print("\n3. Checking templates/history.html...")
with open('templates/history.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
    
    checks = [
        ('<th>Delete</th>', 'Delete column header'),
        ('🗑️ Delete', 'Delete button'),
        ('viewSymptomDetails', 'View details function'),
        ('Symptom Analysis - Complete Report', 'Modal title')
    ]
    
    for check_str, description in checks:
        if check_str in html_content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND!")

# Check 4: Database
print("\n4. Checking database...")
try:
    import sqlite3
    conn = sqlite3.connect('data/predictions.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    
    required_columns = ['prediction_type', 'symptoms_data', 'risk_assessment']
    for col in required_columns:
        if col in columns:
            print(f"   ✅ Column '{col}' exists")
        else:
            print(f"   ❌ Column '{col}' NOT FOUND!")
except Exception as e:
    print(f"   ❌ Error checking database: {e}")

# Summary
print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print("\nIf all checks show ✅, the changes are applied correctly.")
print("If you see ❌, please check the file and reapply changes.")
print("\nNext steps:")
print("1. Restart the server (Ctrl+C then python src/app.py)")
print("2. Clear browser cache (Ctrl+Shift+Delete)")
print("3. Hard refresh the page (Ctrl+F5)")
print("=" * 80)
