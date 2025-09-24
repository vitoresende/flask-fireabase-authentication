from flask import Blueprint, request, jsonify, current_app, session, redirect, url_for
import jwt
from datetime import datetime, timedelta
import uuid
import requests
from requests_oauthlib import OAuth2Session
from app.models import User
from app.decorators import authentication_required

auth_bp = Blueprint('auth', __name__)

def generate_jwt_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user with email and password"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validations
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            # If user exists and was created via Google without a password, allow setting password
            if existing_user.google_id and not existing_user.has_password:
                existing_user.set_password(password)
                existing_user.name = name or existing_user.name # Update name if provided
                if existing_user.save():
                    token = generate_jwt_token(existing_user.uid)
                    return jsonify({
                        'success': True,
                        'message': 'Password set for Google-linked account',
                        'data': {
                            'user': {
                                'uid': existing_user.uid,
                                'email': existing_user.email,
                                'name': existing_user.name,
                                'has_password': existing_user.has_password,
                                'google_id': existing_user.google_id is not None
                            },
                            'token': token
                        }
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Error updating Google-linked account'
                    }), 500
            else:
                # Otherwise, email is genuinely in use
                return jsonify({
                    'success': False,
                    'message': 'Email is already in use'
                }), 409
        
        # Create new user
        user_id = str(uuid.uuid4())
        user = User(
            uid=user_id,
            email=email,
            name=name or email.split('@')[0],
            has_password=True
        )
        user.set_password(password)
        
        # Save to database
        if user.save():
            # Generate JWT token
            token = generate_jwt_token(user_id)
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'user': {
                        'uid': user.uid,
                        'email': user.email,
                        'name': user.name,
                        'has_password': user.has_password
                    },
                    'token': token
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error saving user'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with email and password"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = User.find_by_email(email)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Generate JWT token
        token = generate_jwt_token(user.uid)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': {
                    'uid': user.uid,
                    'email': user.email,
                    'name': user.name,
                    'has_password': user.has_password
                },
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500

@auth_bp.route('/set-password', methods=['POST'])
@authentication_required
def set_password():
    """Set password for user who logged in with Google"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        password = data.get('password', '')
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Password is required'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Get current user from request
        user = request.current_user
        
        # Update password
        if user.update_password(password):
            return jsonify({
                'success': True,
                'message': 'Password set successfully',
                'data': {
                    'user': {
                        'uid': user.uid,
                        'email': user.email,
                        'name': user.name,
                        'has_password': True
                    }
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error updating password'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@authentication_required
def get_profile():
    """Get authenticated user profile"""
    try:
        user = request.current_user
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'uid': user.uid,
                    'email': user.email,
                    'name': user.name,
                    'has_password': user.has_password,
                    'google_id': user.google_id is not None
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500

@auth_bp.route('/validate-token', methods=['POST'])
def validate_token():
    """Validate JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Token not provided'
            }), 400
        
        token = data.get('token', '')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token not provided'
            }), 400
        
        try:
            # Decode JWT token
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            # Find user in database
            user = User.find_by_uid(payload['user_id'])
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 401
            
            return jsonify({
                'success': True,
                'message': 'Token is valid',
                'data': {
                    'user': {
                        'uid': user.uid,
                        'email': user.email,
                        'name': user.name,
                        'has_password': user.has_password,
                        'google_id': user.google_id is not None
                    }
                }
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500

# Google OAuth routes
@auth_bp.route('/google/login')
def google_login():
    """Start Google login process"""
    try:
        # Check if Google credentials are configured
        if not current_app.config.get('GOOGLE_CLIENT_ID') or not current_app.config.get('GOOGLE_CLIENT_SECRET'):
            return jsonify({
                'success': False,
                'message': 'Google credentials not configured'
            }), 500
        
        # Configure OAuth2Session
        google = OAuth2Session(
            current_app.config['GOOGLE_CLIENT_ID'],
            scope=['openid', 'email', 'profile'],
            redirect_uri=url_for('auth.google_callback', _external=True)
        )
        
        # Get authorization URL
        authorization_url, state = google.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            access_type='offline',
            prompt='select_account'
        )
        
        # Save state in session
        session['oauth_state'] = state
        
        return redirect(authorization_url)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting Google login: {str(e)}'
        }), 500

@auth_bp.route('/google/callback')
def google_callback():
    """Google OAuth callback"""
    try:
        # Check for error in response
        if 'error' in request.args:
            error_msg = request.args.get('error_description', 'Unknown error')
            return redirect(f'/?error={error_msg}')
        
        # Check state
        if request.args.get('state') != session.get('oauth_state'):
            return redirect('/?error=Invalid OAuth state')
        
        # Configure OAuth2Session
        google = OAuth2Session(
            current_app.config['GOOGLE_CLIENT_ID'],
            state=session['oauth_state'],
            redirect_uri=url_for('auth.google_callback', _external=True)
        )
        
        # Get access token
        token = google.fetch_token(
            'https://oauth2.googleapis.com/token',
            client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
            authorization_response=request.url
        )
        
        # Get user information
        user_info_response = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
        user_info = user_info_response.json()
        
        # Process user data
        google_id = user_info.get('id')
        email = user_info.get('email')
        name = user_info.get('name')
        
        if not google_id or not email:
            return redirect('/?error=Could not get information from Google')
        
        # Check if user already exists
        existing_user = User.find_by_google_id(google_id)
        
        if existing_user:
            # User already exists, login
            user = existing_user
        else:
            # Check if user with same email exists
            email_user = User.find_by_email(email)
            
            if email_user:
                # Associate Google account with existing user
                email_user.google_id = google_id
                if email_user.save():
                    user = email_user
                else:
                    return redirect('/?error=Error associating Google account')
            else:
                # Create new user
                user_id = str(uuid.uuid4())
                user = User(
                    uid=user_id,
                    email=email,
                    name=name,
                    google_id=google_id,
                    has_password=False
                )
                
                if not user.save():
                    return redirect('/?error=Error creating user')
        
        # Generate JWT token
        jwt_token = generate_jwt_token(user.uid)
        
        # Redirect with token (in production, use more secure method)
        return redirect(f'/?token={jwt_token}&user={user.uid}')
        
    except Exception as e:
        return redirect(f'/?error=Google callback error: {str(e)}')

@auth_bp.route('/google/user-info', methods=['POST'])
def google_user_info():
    """Process Google user information (for JavaScript use)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        google_id = data.get('google_id')
        email = data.get('email')
        name = data.get('name')
        
        if not google_id or not email:
            return jsonify({
                'success': False,
                'message': 'Incomplete Google data'
            }), 400
        
        # Check if user already exists
        existing_user = User.find_by_google_id(google_id)
        
        if existing_user:
            # User already exists, login
            user = existing_user
        else:
            # Check if user with same email exists
            email_user = User.find_by_email(email)
            
            if email_user:
                # Associate Google account with existing user
                email_user.google_id = google_id
                if email_user.save():
                    user = email_user
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Error associating Google account'
                    }), 500
            else:
                # Create new user
                user_id = str(uuid.uuid4())
                user = User(
                    uid=user_id,
                    email=email,
                    name=name,
                    google_id=google_id,
                    has_password=False
                )
                
                if not user.save():
                    return jsonify({
                        'success': False,
                        'message': 'Error creating user'
                    }), 500
        
        # Generate JWT token
        jwt_token = generate_jwt_token(user.uid)
        
        return jsonify({
            'success': True,
            'message': 'Google login successful',
            'data': {
                'user': {
                    'uid': user.uid,
                    'email': user.email,
                    'name': user.name,
                    'has_password': user.has_password,
                    'google_id': True
                },
                'token': jwt_token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}'
        }), 500
