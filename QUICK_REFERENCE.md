# 🚀 Quick Reference Card

## 📍 URLs

| Page | URL | Auth Required |
|------|-----|---------------|
| Login | http://localhost:5000/login | No |
| Register | http://localhost:5000/register | No |
| Home | http://localhost:5000 | Yes |
| History | http://localhost:5000/history | Yes |
| Dashboard | http://localhost:5000/dashboard | Yes |
| Profile | http://localhost:5000/profile | Yes |
| API Docs | http://localhost:5000/api/docs | No |
| About | http://localhost:5000/about | No |

## 🔐 Authentication

### Register
```
1. Go to /register
2. Fill in: Full Name, Username, Email, Password
3. Click "Create Account"
```

### Login
```
1. Go to /login
2. Enter: Username, Password
3. Click "Sign In"
```

### Logout
```
Click "Logout" in navigation menu
```

## 🔑 API Tokens

### Create Token
```
1. Login
2. Go to /profile
3. Click "Create Token"
4. Enter name and expiry
5. COPY TOKEN (won't see again!)
```

### Use Token
```
Header: Authorization: Bearer YOUR_TOKEN
```

### Revoke Token
```
1. Go to /profile
2. Find token
3. Click trash icon
```

## 📡 API Endpoints

### Base URL
```
http://localhost:5000/api/v1
```

### Make Prediction
```http
POST /api/v1/predict
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
    "features": [30 numeric values]
}
```

### Get History
```http
GET /api/v1/history?limit=10&offset=0
Authorization: Bearer YOUR_TOKEN
```

### Get Statistics
```http
GET /api/v1/statistics
Authorization: Bearer YOUR_TOKEN
```

### Get Prediction
```http
GET /api/v1/prediction/{id}
Authorization: Bearer YOUR_TOKEN
```

## 💻 Code Examples

### Python
```python
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:5000/api/v1/predict",
    headers=headers,
    json={"features": [17.99, 10.38, ...]}
)

print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, ...]}'
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't access pages | Register and login first |
| Session expired | Login again |
| API 401 error | Check token format: `Bearer TOKEN` |
| Token not working | Create new token |
| Database locked | Restart server |

## 📁 Important Files

| File | Purpose |
|------|---------|
| `src/auth.py` | Authentication system |
| `src/app.py` | Main application |
| `test_api.py` | API testing script |
| `AUTH_API_GUIDE.md` | Complete guide |
| `SETUP_AUTH_API.md` | Setup instructions |
| `NEW_FEATURES_SUMMARY.md` | Feature summary |

## 🎯 Testing Commands

### Start Server
```bash
python src/app.py
```

### Test API
```bash
python test_api.py
```

### Check Health
```bash
curl http://localhost:5000/health
```

## 📊 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

## 🔒 Security Notes

- Passwords are hashed (SHA-256)
- Tokens expire (configurable)
- Sessions are secure
- All routes protected
- API requires authentication

## 📚 Documentation

- **Setup:** `SETUP_AUTH_API.md`
- **Full Guide:** `AUTH_API_GUIDE.md`
- **Features:** `FEATURES.md`
- **API Docs:** http://localhost:5000/api/docs

## ✅ Quick Test

1. Register account
2. Login
3. Create API token
4. Update `test_api.py`
5. Run `python test_api.py`
6. See success! ✅

---

**Student ID:** 10953361  
**Project:** Breast Cancer Detection System  
**Status:** Production Ready ✅
