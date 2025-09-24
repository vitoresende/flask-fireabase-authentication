# 🚀 Quick Start Guide - Flask Firebase PoC

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd flask-firebase-poc
pip3 install -r requirements.txt
```

### 2. Run Application
```bash
python3 run.py
```

### 3. Access Interface
Open your browser at: **http://localhost:5000**

### 4. Test Features
1. **Register a user** in the "Register" tab
2. **Login** with created credentials
3. **Test APIs** using interface buttons
4. **View results** in the output terminal

## 🧪 Automated Tests

Run automated tests:
```bash
python3 test_api.py
```

## 🔧 Optional Configuration

### Google OAuth (Optional)
1. Access [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Configure in `.env` file:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Real Firebase (Optional)
1. Create project in [Firebase Console](https://console.firebase.google.com/)
2. Download `firebase-credentials.json`
3. Place in project root

## 📋 Tested Features

- ✅ **User registration** with validation
- ✅ **Email/password login** 
- ✅ **JWT tokens** with expiration
- ✅ **Protected routes** with decorator
- ✅ **Public and private APIs**
- ✅ **Local Firestore simulator**
- ✅ **Responsive interface**
- ✅ **Automated tests**

## 🎯 Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Login |
| GET | `/api/public` | Public endpoint |
| GET | `/api/protected` | Protected endpoint |
| GET | `/api/user-data` | User data |

## 🔍 Response Structure

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "user": {
      "uid": "user-uuid",
      "email": "user@example.com",
      "name": "User Name"
    },
    "token": "jwt-token-here"
  }
}
```

## 🛠️ Technologies

- **Flask** - Web framework
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Firestore** - Database
- **OAuth 2.0** - Social login
- **Tailwind CSS** - Interface

## 📞 Support

For questions or issues:
1. Check if all dependencies are installed
2. Verify port 5000 is available
3. Run automated tests
4. Check complete README.md

---
**Ready to use! 🎉**
