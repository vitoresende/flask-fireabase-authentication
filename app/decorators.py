from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import User

def authentication_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check if token is in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format. Use: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Access token required'
            }), 401
        
        try:
            # Decode JWT token
            data = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            # Find user in database
            current_user = User.find_by_uid(data['user_id'])
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 401
            
            # Add current user to request context
            request.current_user = current_user
            
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
                'message': f'Token validation error: {str(e)}'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_authentication(f):
    """Decorator for routes that can work with or without authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        request.current_user = None
        
        # Check if token is in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
                
                # Try to decode token
                data = jwt.decode(
                    token, 
                    current_app.config['JWT_SECRET_KEY'], 
                    algorithms=['HS256']
                )
                
                # Find user in database
                current_user = User.find_by_uid(data['user_id'])
                if current_user:
                    request.current_user = current_user
                    
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, IndexError):
                # Invalid or expired token, but continue without authentication
                pass
        
        return f(*args, **kwargs)
    
    return decorated_function
