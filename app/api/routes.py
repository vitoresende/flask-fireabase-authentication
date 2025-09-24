from flask import Blueprint, request, jsonify
from app.decorators import authentication_required, optional_authentication
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/public', methods=['GET'])
def public_endpoint():
    """Public endpoint that doesn't require authentication"""
    return jsonify({
        'success': True,
        'message': 'This is a public endpoint',
        'data': {
            'timestamp': datetime.utcnow().isoformat(),
            'description': 'Anyone can access this endpoint without authentication',
            'public': True
        }
    }), 200

@api_bp.route('/protected', methods=['GET'])
@authentication_required
def protected_endpoint():
    """Protected endpoint that requires authentication"""
    user = request.current_user
    
    return jsonify({
        'success': True,
        'message': 'Access authorized to protected endpoint',
        'data': {
            'timestamp': datetime.utcnow().isoformat(),
            'user': {
                'uid': user.uid,
                'email': user.email,
                'name': user.name
            },
            'description': 'This endpoint can only be accessed with a valid token',
            'protected': True
        }
    }), 200

@api_bp.route('/user-data', methods=['GET'])
@authentication_required
def get_user_data():
    """Endpoint to get specific user data"""
    user = request.current_user
    
    # Simulate user-specific data
    user_data = {
        'profile': {
            'uid': user.uid,
            'email': user.email,
            'name': user.name,
            'has_password': user.has_password,
            'account_type': 'Google' if user.google_id else 'Email/Password',
            'created_at': user.created_at if isinstance(user.created_at, str) else (user.created_at.isoformat() if user.created_at else None)
        },
        'preferences': {
            'theme': 'light',
            'language': 'en-US',
            'notifications': True
        },
        'stats': {
            'login_count': 1,
            'last_login': datetime.utcnow().isoformat()
        }
    }
    
    return jsonify({
        'success': True,
        'message': 'User data retrieved successfully',
        'data': user_data
    }), 200

@api_bp.route('/admin', methods=['GET'])
@authentication_required
def admin_endpoint():
    """Administrative endpoint (simulated)"""
    user = request.current_user
    
    # Simulate admin permission check
    # In a real system, you would check roles/permissions in the database
    is_admin = user.email.endswith('@admin.com')  # Simple simulation
    
    if not is_admin:
        return jsonify({
            'success': False,
            'message': 'Access denied. Administrator permissions required.'
        }), 403
    
    return jsonify({
        'success': True,
        'message': 'Access authorized to admin panel',
        'data': {
            'timestamp': datetime.utcnow().isoformat(),
            'admin_user': {
                'uid': user.uid,
                'email': user.email,
                'name': user.name
            },
            'admin_data': {
                'total_users': 42,  # Simulated data
                'active_sessions': 15,
                'system_status': 'operational'
            }
        }
    }), 200

@api_bp.route('/mixed', methods=['GET'])
@optional_authentication
def mixed_endpoint():
    """Endpoint that works with or without authentication"""
    user = request.current_user
    
    if user:
        # Authenticated user - return personalized data
        return jsonify({
            'success': True,
            'message': 'Personalized data for authenticated user',
            'data': {
                'timestamp': datetime.utcnow().isoformat(),
                'authenticated': True,
                'user': {
                    'uid': user.uid,
                    'email': user.email,
                    'name': user.name
                },
                'personalized_content': [
                    'Welcome back, ' + user.name + '!',
                    'You have 3 pending notifications',
                    'Your last access was 2 hours ago'
                ]
            }
        }), 200
    else:
        # Unauthenticated user - return generic data
        return jsonify({
            'success': True,
            'message': 'Public data for unauthenticated user',
            'data': {
                'timestamp': datetime.utcnow().isoformat(),
                'authenticated': False,
                'generic_content': [
                    'Welcome to our system!',
                    'Sign in to see personalized content',
                    'Register for free'
                ]
            }
        }), 200

@api_bp.route('/test-token', methods=['POST'])
def test_token():
    """Endpoint to test token validation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        token = data.get('token', '')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token not provided',
                'test_result': 'FAIL - No token provided'
            }), 400
        
        # Test token using validation endpoint
        import jwt
        from flask import current_app
        from app.models import User
        
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
                    'message': 'User not found',
                    'test_result': 'FAIL - User not found'
                }), 401
            
            return jsonify({
                'success': True,
                'message': 'Token is valid',
                'test_result': 'PASS - Token is valid',
                'data': {
                    'user': {
                        'uid': user.uid,
                        'email': user.email,
                        'name': user.name
                    },
                    'token_info': {
                        'expires_at': datetime.fromtimestamp(payload['exp']).isoformat(),
                        'issued_at': datetime.fromtimestamp(payload['iat']).isoformat()
                    }
                }
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expired',
                'test_result': 'FAIL - Token expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token',
                'test_result': 'FAIL - Invalid token'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Internal error: {str(e)}',
            'test_result': f'ERROR - {str(e)}'
        }), 500
