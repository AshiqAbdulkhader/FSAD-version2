from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import query_db

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

def role_required(*allowed_roles):
    """Decorator to require specific role(s)"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user_id = get_jwt_identity()
            # Get user role from database
            user = query_db(
                'SELECT role FROM users WHERE id = %s',
                (user_id,),
                fetch_one=True
            )
            
            if not user or user[0] not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = query_db(
        'SELECT id, email, name, role FROM users WHERE id = %s',
        (user_id,),
        fetch_one=True
    )
    if user:
        return {
            'id': user[0],
            'email': user[1],
            'name': user[2],
            'role': user[3]
        }
    return None

