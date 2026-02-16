# Authentication & REST API Guide

## 🔐 New Features Added

Your Breast Cancer Detection System now includes:

1. **User Authentication System**
   - User registration and login
   - Secure password hashing
   - Session management
   - Protected routes

2. **REST API with Token Authentication**
   - API token generation and management
   - Token-based authentication
   - RESTful endpoints for predictions
   - Comprehensive API documentation

---

## 🚀 Quick Start

### 1. First Time Setup

The authentication system will automatically create the necessary database when you first run the application.

```bash
# Start the application
python src/app.py
```

### 2. Create Your Account

1. Open http://localhost:5000
2. You'll be redirected to the login page
3. Click "Register here"
4. Fill in your details:
   - Full Name
   - Username (3-20 characters)
   - Email
   - Password (minimum 6 characters)
5. Click "Create Account"

### 3. Login

1. Enter your username and password
2. Click "Sign In"
3. You'll be redirected to the main application

---

## 🔑 API Token Management

### Creating an API Token

1. Log in to your account
2. Click "Profile" in the navigation menu
3. In the "API Tokens" section, click "Create Token"
4. Enter a name for your token (e.g., "My Application")
5. Select expiry period (30 days, 90 days, 1 year, or never)
6. Click "Create Token"
7. **IMPORTANT:** Copy the token immediately - you won't see it again!

### Using Your API Token

Include your token in the `Authorization` header of your API requests:

```bash
Authorization: Bearer YOUR_API_TOKEN_HERE
```

### Managing Tokens

- View all your tokens in the Profile page
- See when each token was created and last used
- Revoke tokens you no longer need
- Active tokens show a green "Active" badge
- Revoked tokens show a gray "Revoked" badge

---

## 📡 REST API Usage

### Base URL

```
http://localhost:5000/api/v1
```

### Authentication

All API endpoints require authentication. Include your API token in the header:

```bash
Authorization: Bearer YOUR_API_TOKEN
```

---

## 🎯 API Endpoints

### 1. Make a Prediction

**Endpoint:** `POST /api/v1/predict`

**Request:**
```json
{
    "features": [
        17.99, 10.38, 122.8, 1001, 0.1184,
        0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
        1.095, 0.9053, 8.589, 153.4, 0.006399,
        0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
        25.38, 17.33, 184.6, 2019, 0.1622,
        0.6656, 0.7119, 0.2654, 0.4601, 0.1189
    ]
}
```

**Response:**
```json
{
    "success": true,
    "prediction_id": 123,
    "prediction": 1,
    "prediction_label": "Malignant",
    "confidence": 98.5,
    "model_used": "Logistic Regression",
    "all_models": {
        "Logistic Regression": {"prediction": 1, "confidence": 98.5},
        "Random Forest": {"prediction": 1, "confidence": 97.2},
        "SVM": {"prediction": 1, "confidence": 96.8}
    },
    "feature_importance": [...],
    "risk_assessment": {
        "level": "High",
        "message": "Immediate medical consultation recommended"
    },
    "timestamp": "2024-01-01T12:00:00",
    "user": "your_username"
}
```

### 2. Get Prediction History

**Endpoint:** `GET /api/v1/history?limit=10&offset=0`

**Response:**
```json
{
    "success": true,
    "predictions": [
        {
            "id": 123,
            "timestamp": "2024-01-01T12:00:00",
            "prediction": 1,
            "prediction_label": "Malignant",
            "confidence": 98.5,
            "model_name": "Logistic Regression"
        }
    ],
    "total": 150,
    "limit": 10,
    "offset": 0,
    "user": "your_username"
}
```

### 3. Get Statistics

**Endpoint:** `GET /api/v1/statistics`

**Response:**
```json
{
    "success": true,
    "statistics": {
        "total_predictions": 150,
        "benign_count": 100,
        "malignant_count": 50,
        "average_confidence": 95.5,
        "predictions_last_7_days": 25
    },
    "user": "your_username"
}
```

### 4. Get Specific Prediction

**Endpoint:** `GET /api/v1/prediction/{prediction_id}`

**Response:**
```json
{
    "success": true,
    "prediction": {
        "id": 123,
        "timestamp": "2024-01-01T12:00:00",
        "prediction": 1,
        "prediction_label": "Malignant",
        "confidence": 98.5,
        "model_name": "Logistic Regression",
        "features": [...],
        "all_model_predictions": {...}
    },
    "user": "your_username"
}
```

---

## 💻 Code Examples

### Python Example

```python
import requests
import json

# Configuration
API_TOKEN = "your_api_token_here"
BASE_URL = "http://localhost:5000/api/v1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Example features (30 values)
features = [
    17.99, 10.38, 122.8, 1001, 0.1184,
    0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
    1.095, 0.9053, 8.589, 153.4, 0.006399,
    0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
    25.38, 17.33, 184.6, 2019, 0.1622,
    0.6656, 0.7119, 0.2654, 0.4601, 0.1189
]

# Make prediction
response = requests.post(
    f"{BASE_URL}/predict",
    headers=headers,
    json={"features": features}
)

if response.status_code == 200:
    result = response.json()
    print(f"Prediction: {result['prediction_label']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Model Used: {result['model_used']}")
    print(f"Risk Level: {result['risk_assessment']['level']}")
else:
    print(f"Error: {response.json()}")

# Get history
response = requests.get(
    f"{BASE_URL}/history?limit=5",
    headers=headers
)

if response.status_code == 200:
    history = response.json()
    print(f"\nTotal Predictions: {history['total']}")
    for pred in history['predictions']:
        print(f"- ID {pred['id']}: {pred['prediction_label']} ({pred['confidence']}%)")

# Get statistics
response = requests.get(
    f"{BASE_URL}/statistics",
    headers=headers
)

if response.status_code == 200:
    stats = response.json()['statistics']
    print(f"\nStatistics:")
    print(f"- Total: {stats['total_predictions']}")
    print(f"- Benign: {stats['benign_count']}")
    print(f"- Malignant: {stats['malignant_count']}")
```

### JavaScript (Node.js) Example

```javascript
const axios = require('axios');

const API_TOKEN = 'your_api_token_here';
const BASE_URL = 'http://localhost:5000/api/v1';

const headers = {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json'
};

// Example features (30 values)
const features = [
    17.99, 10.38, 122.8, 1001, 0.1184,
    0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
    1.095, 0.9053, 8.589, 153.4, 0.006399,
    0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
    25.38, 17.33, 184.6, 2019, 0.1622,
    0.6656, 0.7119, 0.2654, 0.4601, 0.1189
];

// Make prediction
async function makePrediction() {
    try {
        const response = await axios.post(
            `${BASE_URL}/predict`,
            { features },
            { headers }
        );
        
        console.log('Prediction:', response.data.prediction_label);
        console.log('Confidence:', response.data.confidence + '%');
        console.log('Model Used:', response.data.model_used);
        console.log('Risk Level:', response.data.risk_assessment.level);
    } catch (error) {
        console.error('Error:', error.response.data);
    }
}

// Get history
async function getHistory() {
    try {
        const response = await axios.get(
            `${BASE_URL}/history?limit=5`,
            { headers }
        );
        
        console.log('\nTotal Predictions:', response.data.total);
        response.data.predictions.forEach(pred => {
            console.log(`- ID ${pred.id}: ${pred.prediction_label} (${pred.confidence}%)`);
        });
    } catch (error) {
        console.error('Error:', error.response.data);
    }
}

// Get statistics
async function getStatistics() {
    try {
        const response = await axios.get(
            `${BASE_URL}/statistics`,
            { headers }
        );
        
        const stats = response.data.statistics;
        console.log('\nStatistics:');
        console.log('- Total:', stats.total_predictions);
        console.log('- Benign:', stats.benign_count);
        console.log('- Malignant:', stats.malignant_count);
    } catch (error) {
        console.error('Error:', error.response.data);
    }
}

// Run all examples
makePrediction();
getHistory();
getStatistics();
```

### cURL Examples

```bash
# Make a prediction
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
  }'

# Get history
curl -X GET "http://localhost:5000/api/v1/history?limit=10" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Get statistics
curl -X GET http://localhost:5000/api/v1/statistics \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Get specific prediction
curl -X GET http://localhost:5000/api/v1/prediction/123 \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

---

## 🔒 Security Best Practices

### For Users

1. **Strong Passwords**
   - Use at least 8 characters
   - Mix uppercase, lowercase, numbers, and symbols
   - Don't reuse passwords from other sites

2. **API Token Security**
   - Never share your API tokens
   - Don't commit tokens to version control
   - Use environment variables for tokens in code
   - Revoke tokens you no longer need
   - Create separate tokens for different applications

3. **Session Management**
   - Log out when done
   - Don't use public computers for sensitive operations

### For Developers

1. **Environment Variables**
```python
import os
API_TOKEN = os.getenv('BREAST_CANCER_API_TOKEN')
```

2. **Token Storage**
   - Store tokens in `.env` files (add to `.gitignore`)
   - Use secret management services in production
   - Never hardcode tokens in source code

3. **Error Handling**
```python
try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
```

---

## 📊 API Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Invalid or missing API token |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error occurred |

---

## 🐛 Troubleshooting

### "No authorization token provided"
- Make sure you're including the `Authorization` header
- Format: `Authorization: Bearer YOUR_TOKEN`
- Check for typos in the header name

### "Invalid or expired token"
- Token may have expired
- Token may have been revoked
- Create a new token in the Profile page

### "Invalid feature count"
- Ensure you're sending exactly 30 feature values
- Check that all values are numbers
- Verify JSON format is correct

### "Prediction failed"
- Check that feature values are in valid ranges
- Ensure all values are numeric
- Review server logs for detailed error messages

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:5000/api/docs
- **Profile & Tokens**: http://localhost:5000/profile
- **Main Application**: http://localhost:5000

---

## 🎓 For Your Project Report

### What to Highlight:

1. **Security Implementation**
   - Password hashing (SHA-256)
   - Session management
   - Token-based API authentication
   - Protected routes

2. **RESTful API Design**
   - Standard HTTP methods (GET, POST, DELETE)
   - JSON request/response format
   - Proper status codes
   - Comprehensive documentation

3. **User Experience**
   - Clean authentication UI
   - Token management interface
   - API documentation page
   - Error handling and feedback

4. **Integration Capabilities**
   - External system integration via API
   - Multiple programming language support
   - Scalable architecture
   - Production-ready features

---

## 🚀 Next Steps

1. **Test the Authentication**
   - Create an account
   - Log in and out
   - Test session persistence

2. **Generate API Token**
   - Create your first token
   - Test it with cURL or Python
   - Try all API endpoints

3. **Build an Integration**
   - Use the code examples
   - Create a simple client application
   - Test error handling

4. **Document Your Work**
   - Screenshot the authentication flow
   - Document API usage in your report
   - Explain security measures

---

## 📝 Summary

You now have a complete, production-ready system with:

✅ User authentication and authorization
✅ Secure API token management
✅ RESTful API endpoints
✅ Comprehensive API documentation
✅ Code examples in multiple languages
✅ Security best practices
✅ Professional error handling

This significantly enhances your project's scope and demonstrates advanced software engineering skills!

---

**Student ID:** 10953361  
**Project:** AI-Based Breast Cancer Detection System  
**Features:** Authentication, REST API, Token Management
