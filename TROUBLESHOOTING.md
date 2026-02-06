# Troubleshooting Guide

## Issue: No Results After Submitting File

### Fixed Issues:
✅ Updated CSV parsing to handle headers correctly
✅ Added better error messages
✅ Added console logging for debugging

### How to Test:

#### Option 1: Upload CSV File
1. Go to http://localhost:5000
2. Click "Choose File" under "Upload Patient Data"
3. Select any file from `test_samples/` folder (e.g., `benign_sample_1.csv`)
4. Click "Analyze Now"
5. Wait for results (should appear in 2-3 seconds)

#### Option 2: Manual Input (Easier to Test)
1. Go to http://localhost:5000
2. Paste this in the "Enter Features Manually" field:
```
13.54,14.36,87.46,566.3,0.09779,0.08129,0.06664,0.04781,0.1885,0.05766,0.2699,0.7886,2.058,23.56,0.008462,0.0146,0.02387,0.01315,0.0198,0.0023,15.11,19.26,99.7,711.2,0.144,0.1773,0.239,0.1288,0.2977,0.07259
```
3. Click "Analyze Now"
4. You should see results immediately

### Expected Results:
- ✅ Prediction: Benign
- ✅ Confidence: ~98%
- ✅ Model comparison table (3 models)
- ✅ Top 5 contributing features
- ✅ Download PDF Report button

### Debugging Steps:

#### 1. Check Browser Console
- Press F12 to open Developer Tools
- Go to "Console" tab
- Look for any error messages
- You should see logs like:
  - "Features from text input: 30" or "Parsed features: 30"
  - "Sending prediction request..."
  - "Response status: 200"
  - "Prediction result: {...}"

#### 2. Check Network Tab
- Press F12 → Network tab
- Submit a prediction
- Look for `/predict` request
- Check if it's Status 200 (success)
- Click on it to see Request/Response

#### 3. Check Server Logs
- Look at the terminal where you ran `python src/app.py`
- Should see prediction requests being processed
- Warnings about feature names are normal (not errors)

### Common Issues:

#### Issue: "Expected 30 features, got X"
**Solution:** 
- Make sure your CSV has exactly 30 numeric columns
- Check that there are no extra commas or missing values
- Use the test files in `test_samples/` folder

#### Issue: "Invalid feature values"
**Solution:**
- Ensure all values are numbers (not text)
- No empty values
- Use decimal point (.) not comma (,) for decimals

#### Issue: "Please provide input data"
**Solution:**
- Either upload a file OR enter text manually
- Don't leave both empty

#### Issue: Nothing happens when clicking "Analyze Now"
**Solution:**
1. Check browser console for JavaScript errors
2. Make sure the server is running
3. Try refreshing the page (Ctrl+F5)
4. Clear browser cache

### Server Not Starting?

If you see errors when running `python src/app.py`:

1. **ModuleNotFoundError: No module named 'reportlab'**
   ```cmd
   pip install reportlab plotly
   ```

2. **Models not found**
   ```cmd
   python src/train_model.py
   ```

3. **Port already in use**
   - Stop the existing server (Ctrl+C)
   - Or change port in `src/app.py`

### Still Not Working?

1. **Restart everything:**
   ```cmd
   # Stop server (Ctrl+C)
   # Restart
   python src/app.py
   ```

2. **Clear browser cache:**
   - Press Ctrl+Shift+Delete
   - Clear cached images and files
   - Refresh page (Ctrl+F5)

3. **Check file format:**
   - Open your CSV in Notepad
   - Should have 30 numbers separated by commas
   - No extra spaces or special characters

4. **Use test data:**
   - Copy from `test_samples/manual_input_example.txt`
   - Paste into manual input field
   - This is guaranteed to work

### Success Indicators:

When working correctly, you should see:
- ✅ Loading spinner appears
- ✅ Button shows "Analyzing..."
- ✅ Results appear within 2-3 seconds
- ✅ Green (Benign) or Red (Malignant) result card
- ✅ Confidence percentage
- ✅ Model comparison table
- ✅ Feature importance bars
- ✅ Download PDF button

### Contact Information:

If issues persist:
1. Check browser console (F12)
2. Check server terminal output
3. Try the manual input method first
4. Use the provided test files

### Quick Test Command:

To verify the system is working, open browser console and run:
```javascript
fetch('/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        features: [13.54,14.36,87.46,566.3,0.09779,0.08129,0.06664,0.04781,0.1885,0.05766,0.2699,0.7886,2.058,23.56,0.008462,0.0146,0.02387,0.01315,0.0198,0.0023,15.11,19.26,99.7,711.2,0.144,0.1773,0.239,0.1288,0.2977,0.07259]
    })
}).then(r => r.json()).then(console.log);
```

This should return a prediction result object.
