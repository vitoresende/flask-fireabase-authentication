# Flask Firebase PoC - Complete Authentication System

This project is a **Proof of Concept (PoC)** that demonstrates a complete authentication system using **Flask** and **Firebase**, including email/password login and **Google OAuth 2.0** integration.

## 🚀 Features

### Back-end (Flask)
- ✅ **Modular structure** with blueprints (`auth.py` and `api.py`)
- ✅ **Secure authentication** with Flask-Bcrypt (password hashing with salt)
- ✅ **JWT Tokens** for authorization (PyJWT)
- ✅ **Google OAuth 2.0** integration with requests-oauthlib
- ✅ **Firestore integration** (with local simulator for development)
- ✅ **@authentication_required decorator** to protect routes
- ✅ **Mock endpoints** to demonstrate functionality

### Front-end
- ✅ **Responsive interface** with Tailwind CSS
- ✅ **Complete authentication system** (login/register)
- ✅ **Google OAuth 2.0 login** implementation
- ✅ **Password setting** for Google users
- ✅ **Interactive API testing** with visual feedback
- ✅ **State management** and session persistence

### Security Features
- ✅ **Password hashing with salt** (never stored in plain text)
- ✅ **Secure JWT tokens** with configurable expiration
- ✅ **Token validation** on all protected routes
- ✅ **CORS configuration** for development
- ✅ **Robust error handling** without information leakage

## 📁 Project Structure

```
flask-firebase-poc/
├── app/
│   ├── __init__.py              # Main application configuration
│   ├── config.py                # Settings and environment variables
│   ├── models.py                # User data model
│   ├── decorators.py            # Authentication decorators
│   ├── firestore_simulator.py   # Local Firestore simulator
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py            # Authentication routes
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API routes
│   └── static/
│       ├── index.html           # User interface
│       └── app.js               # Frontend JavaScript
├── requirements.txt             # Python dependencies
├── run.py                       # Main file to run the application
├── .env                         # Environment variables (development)
├── .env.example                 # Configuration example
├── firebase-credentials-example.json  # Firebase credentials example
├── test_api.py                  # Automated test script
├── QUICK_START.md               # Quick start guide
└── README.md                    # This documentation
```

## 🛠️ Installation and Setup

### 1. Prerequisites
- Python 3.8+
- pip3

### 2. Install Dependencies
```bash
cd flask-firebase-poc
pip3 install -r requirements.txt
```

### 3. Environment Configuration

#### Option A: Local Development (Simulator)
For quick development, the project is already configured to use a local Firestore simulator:

```bash
cp .env.example .env
# Edit the .env file with your settings
```

#### Option B: Real Firebase (Production)
1. Create a project in [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Download service account credentials
4. Rename to `firebase-credentials.json`
5. Configure variables in `.env` file

### 4. Google OAuth Configuration (Optional)
1. Access [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select an existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Configure redirect URLs:
   - `http://localhost:5000/auth/google/callback` (development)
6. Add credentials to `.env` file:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

## 🔐 Complete Configuration Guide

### Getting Firebase Credentials

The `firebase-credentials.json` file is a **Service Account Key** required for the Firebase Admin SDK:

#### Step by step:
1. Access [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click the **gear** ⚙️ → **Project settings**
4. Go to **"Service accounts"** tab
5. Click **"Generate new private key"**
6. Download the JSON file
7. Rename to `firebase-credentials.json`
8. Place in project root

#### File structure:
```json
{
  "type": "service_account",
  "project_id": "your-firebase-project",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

### Setting up Firestore

In Firebase Console:
1. Go to **"Firestore Database"**
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for development)
4. Select a location

### Getting Google OAuth Credentials

#### Step by step:
1. Access [Google Cloud Console](https://console.cloud.google.com/)
2. Select the **same project** as Firebase
3. Go to **"APIs & Services"** → **"Credentials"**
4. Click **"+ CREATE CREDENTIALS"** → **"OAuth 2.0 Client ID"**
5. Choose **"Web application"**
6. Configure:
   - **Name**: Flask Firebase PoC
   - **Authorized redirect URIs**:
     - `http://localhost:5000/auth/google/callback`
     - `http://127.0.0.1:5000/auth/google/callback`
7. Click **"Create"**
8. Copy the **Client ID** and **Client Secret**

### Complete .env File

Based on your Firebase config, create the `.env` file:

```bash
# Application settings
SECRET_KEY=FlaskFirebasePoc2024_SecureKey_9x7m2n8p4q1w5e6r3t9y0u8i7o6p5a4s2d1f
JWT_SECRET_KEY=JWTAuth_SuperSecure_2024_k8j7h6g5f4d3s2a1q9w8e7r6t5y4u3i2o1p0z9x8c7v6b5n4m3

# Google OAuth (obtained from Google Cloud Console)
GOOGLE_CLIENT_ID=123456789-abcdef.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret_here

# Firebase (use projectId from your firebaseConfig)
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json

# Development settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Configuration Mapping

#### From your firebaseConfig to .env:
```javascript
// Your firebaseConfig (frontend)
const firebaseConfig = {
  projectId: "my-project-123"  // ← Use this value
};
```

```bash
# In .env file (backend)
FIREBASE_PROJECT_ID=my-project-123
```

## 🚀 Running the Application

```bash
python3 run.py
```

The application will be available at: `http://localhost:5000`

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/set-password` - Set password (Google users)
- `GET /auth/profile` - Get authenticated user profile
- `POST /auth/validate-token` - Validate JWT token
- `GET /auth/google/login` - Start Google login
- `GET /auth/google/callback` - Google OAuth callback

### API
- `GET /api/public` - Public endpoint (no authentication)
- `GET /api/protected` - Protected endpoint (requires token)
- `GET /api/user-data` - User-specific data
- `GET /api/mixed` - Endpoint that works with/without authentication
- `GET /api/admin` - Administrative endpoint (simulated)
- `POST /api/test-token` - Test token validation

## 🧪 Testing the Application

### Web Interface
1. Access `http://localhost:5000`
2. Register a new user or login
3. Use test buttons to verify APIs
4. Test Google login (if configured)

### Automated Tests
```bash
python3 test_api.py
```

### Manual Tests via cURL

#### Register user:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'
```

#### Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

#### Test protected endpoint:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/protected
```

## 🔧 Technologies Used

### Back-end
- **Flask 2.3.3** - Web framework
- **Flask-CORS 4.0.0** - CORS support
- **Flask-Bcrypt 1.0.1** - Password hashing
- **PyJWT 2.8.0** - JWT tokens
- **requests-oauthlib 1.3.1** - OAuth 2.0
- **firebase-admin 6.2.0** - Firebase SDK
- **google-cloud-firestore 2.11.1** - Firestore client
- **python-dotenv 1.0.0** - Environment variables

### Front-end
- **HTML5** - Structure
- **Tailwind CSS 2.2.19** - Styling
- **Font Awesome 6.0.0** - Icons
- **JavaScript ES6+** - Interactive functionality

## 🔒 Security Features

1. **Password Hashing**: All passwords stored with bcrypt hash and salt
2. **JWT Tokens**: Stateless authentication with secure tokens
3. **Token Validation**: Automatic verification on protected routes
4. **CORS**: Properly configured for frontend requests
5. **Error Handling**: Standardized responses without sensitive information leakage
6. **OAuth 2.0**: Secure integration with Google

## 📝 Demonstrated Features

### Authentication
- [x] User registration with validation
- [x] Email and password login
- [x] Google OAuth 2.0 login
- [x] Password setting for Google users
- [x] Logout with session cleanup

### Authorization
- [x] JWT tokens with expiration
- [x] Route protection decorator
- [x] Automatic token validation
- [x] Different access levels

### Interface
- [x] Responsive and modern design
- [x] Visual feedback for actions
- [x] Interactive API testing
- [x] Frontend state management

## ⚡ Quick Start (5 minutes)

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

## 🚀 Production Deployment

### Next Steps for Production:
1. **Configure real Firebase** with production credentials
2. **Implement HTTPS** with SSL certificates
3. **Set up WSGI server** (Gunicorn + Nginx)
4. **Add rate limiting** to prevent attacks
5. **Implement structured logging**
6. **Configure monitoring** and alerts
7. **Add automated tests**
8. **Implement CI/CD**

### Environment Variables for Production:
```bash
# Generate secure keys for production
SECRET_KEY=your-production-secret-key-here
JWT_SECRET_KEY=your-production-jwt-key-here

# Production Firebase
FIREBASE_PROJECT_ID=your-production-project
FIREBASE_CREDENTIALS_PATH=/path/to/production/credentials.json

# Production Google OAuth
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret

# Production settings
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🛡️ Security Best Practices

### For Development:
✅ Use the generated keys provided

### For Production:
🚨 **ALWAYS generate new keys** for production:

```python
# Script to generate new keys
import secrets
import string

def generate_secret_key(length=64):
    alphabet = string.ascii_letters + string.digits + "_-"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

print("SECRET_KEY=" + generate_secret_key())
print("JWT_SECRET_KEY=" + generate_secret_key())
```

### Security Checklist:
- [ ] Never share keys publicly
- [ ] Use environment variables in production
- [ ] Generate different keys for each environment
- [ ] Keep secure backup of production keys
- [ ] Rotate keys periodically
- [ ] Use HTTPS in production
- [ ] Configure proper CORS origins
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Monitor for suspicious activity

## 🔍 API Response Structure

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "user": {
      "uid": "user-uuid-here",
      "email": "user@example.com",
      "name": "User Name"
    },
    "token": "jwt-token-here"
  }
}
```

## 🐛 Troubleshooting

### Common Issues:

#### 1. Application won't start
- Check if all dependencies are installed: `pip3 install -r requirements.txt`
- Verify Python version: `python3 --version` (should be 3.8+)
- Check if port 5000 is available: `lsof -i :5000`

#### 2. Firebase connection errors
- Verify `firebase-credentials.json` exists and is valid
- Check `FIREBASE_PROJECT_ID` in `.env` matches your project
- For development, the simulator will be used automatically

#### 3. Google OAuth not working
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`
- Check redirect URIs in Google Cloud Console
- Ensure the same project is used for Firebase and Google OAuth

#### 4. Token validation errors
- Check if `JWT_SECRET_KEY` is set in `.env`
- Verify token format: `Bearer <token>`
- Check token expiration (default: 1 hour)

#### 5. CORS errors
- Verify Flask-CORS is installed
- Check if frontend and backend are on same domain
- For production, configure proper CORS origins

### Debug Mode:
```bash
# Enable debug logging
export FLASK_DEBUG=True
python3 run.py
```

### Test Configuration:
```bash
# Test if configuration is loaded correctly
python3 -c "from app import create_app; app = create_app(); print('Configuration loaded successfully')"
```

## 📞 Support

For questions or issues:
1. Check if all dependencies are installed
2. Verify port 5000 is available
3. Run automated tests: `python3 test_api.py`
4. Check this complete documentation
5. Review error logs in terminal

## 📄 License

This project is a PoC for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. For improvements or suggestions, feel free to create issues or pull requests.

---

**Developed with ❤️ using Flask and Firebase**

## 📋 Configuration Summary

### Required Files:
- `.env` - Environment variables
- `firebase-credentials.json` - Firebase service account (optional for development)

### Required Environment Variables:
```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
GOOGLE_CLIENT_ID=your-google-client-id (optional)
GOOGLE_CLIENT_SECRET=your-google-client-secret (optional)
FIREBASE_PROJECT_ID=your-firebase-project-id (optional)
```

### Optional Configuration:
- Google OAuth for social login
- Real Firebase for production database
- Custom JWT expiration time
- Production security settings

The application works out of the box with the local simulator for immediate testing and development! 🎉
