# Symptom Analysis History Feature Update

## Overview
This update enhances the prediction history page to display detailed information about symptom-based predictions, including risk assessments and symptom details.

## Changes Made

### 1. Database Schema Updates (`src/database.py`)
Added three new columns to the `predictions` table:
- **`prediction_type`** (TEXT): Identifies the type of prediction ('symptom' or 'manual')
- **`symptoms_data`** (TEXT): Stores the JSON-encoded symptom data
- **`risk_assessment`** (TEXT): Stores the JSON-encoded risk assessment results

### 2. Database Methods Updated
- **`save_prediction()`**: Now accepts additional parameters for symptom data
  - `prediction_type`: Type of prediction ('symptom' or 'manual')
  - `symptoms_data`: Dictionary of symptom inputs
  - `risk_assessment`: Risk assessment results

- **`get_all_predictions()`**: Returns predictions with symptom data and risk assessment
- **`get_prediction_by_id()`**: Returns full prediction details including symptoms

### 3. Application Updates (`src/app.py`)
- **`predict_symptoms()`** endpoint: Now saves symptom data and risk assessment to database

### 4. History Page Updates (`templates/history.html`)
Enhanced the history table to show:
- **Type Column**: Displays whether prediction is from symptom analysis or manual input
- **Risk Level Column**: Shows the risk assessment level with color-coded badges
- **View Details Button**: For symptom-based predictions, allows viewing full symptom details
- **Symptom Details Modal**: Displays comprehensive symptom information including:
  - Patient information (age, family history, etc.)
  - Physical symptoms (lump, pain, skin changes, etc.)
  - Risk assessment with identified risk factors
  - Medical recommendations

### 5. Migration Script (`migrate_database.py`)
Created a database migration script to add new columns to existing databases without losing data.

## Features

### History Table Enhancements
1. **Prediction Type Badge**:
   - 🩺 Symptom Analysis (blue badge)
   - 📊 Manual Input (gray badge)

2. **Risk Level Display**:
   - Very High (red)
   - High (orange)
   - Moderate (blue)
   - Low-Moderate (primary blue)
   - Low (green)
   - N/A (gray) for manual predictions

3. **Symptom Details Modal**:
   - Patient demographics and history
   - Complete symptom checklist
   - Risk assessment summary
   - Identified risk factors
   - Medical recommendations

## Usage

### For Users
1. Navigate to the History page
2. View all predictions with their types and risk levels
3. Click "👁️ View Details" on symptom-based predictions to see full symptom analysis
4. Download reports as usual

### For Developers
```python
# Save a symptom-based prediction
prediction_id = db.save_prediction(
    prediction=result['prediction'],
    confidence=result['confidence'],
    model_name='Random Forest',
    features=features,
    all_predictions=all_models,
    prediction_type='symptom',
    symptoms_data=symptom_dict,
    risk_assessment=risk_dict
)

# Retrieve with symptom data
prediction = db.get_prediction_by_id(prediction_id)
if prediction['prediction_type'] == 'symptom':
    symptoms = prediction['symptoms_data']
    risk = prediction['risk_assessment']
```

## Migration Instructions

### For Existing Installations
Run the migration script to update your database:
```bash
python migrate_database.py
```

This will:
- Add new columns to existing predictions table
- Preserve all existing data
- Set default values for existing records

### For New Installations
No migration needed - the database will be created with the new schema automatically.

## Testing

Run the test script to verify the feature:
```bash
python test_symptom_history.py
```

This will:
- Create a test symptom-based prediction
- Verify data is saved correctly
- Retrieve and display the prediction
- Show statistics by prediction type

## Benefits

1. **Better Tracking**: Distinguish between symptom-based and manual predictions
2. **Risk Visibility**: See risk assessments at a glance in the history table
3. **Detailed Analysis**: View complete symptom details for any symptom-based prediction
4. **Audit Trail**: Full record of what symptoms were reported
5. **Medical Context**: Risk factors and recommendations preserved for review

## Backward Compatibility

- Existing predictions are automatically marked as 'manual' type
- All existing functionality remains unchanged
- Reports work for both symptom-based and manual predictions
- No breaking changes to existing API endpoints

## Future Enhancements

Potential improvements:
- Filter history by prediction type
- Export symptom data to CSV
- Compare symptoms across multiple predictions
- Trend analysis for symptom-based predictions
- Integration with appointment system for high-risk cases

## Technical Details

### Database Schema
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    prediction INTEGER,
    prediction_label TEXT,
    confidence REAL,
    model_name TEXT,
    features TEXT,
    all_model_predictions TEXT,
    prediction_type TEXT DEFAULT 'manual',
    symptoms_data TEXT,
    risk_assessment TEXT
);
```

### Symptom Data Structure
```json
{
    "age": 45,
    "lump": "small",
    "pain": "mild",
    "skin_change": "none",
    "nipple_discharge": "none",
    "family_history": "yes",
    "nipple_retraction": "none",
    "armpit_lump": "none",
    "breast_shape_change": "minor",
    "skin_texture": "normal",
    "symptom_duration": "weeks",
    "lump_mobility": "mobile",
    "pain_duration": "weeks",
    "menstrual_status": "premenopausal",
    "previous_conditions": "none",
    "pregnancy_history": "parous"
}
```

### Risk Assessment Structure
```json
{
    "risk_level": "Moderate",
    "risk_score": 6,
    "risk_factors": [
        "Age over 40 (45 years)",
        "Small lump detected",
        "Family history of breast cancer"
    ],
    "recommendation": "Medical consultation recommended soon"
}
```

## Support

For issues or questions:
1. Check the test script output
2. Verify database migration completed successfully
3. Check browser console for JavaScript errors
4. Review server logs for API errors
