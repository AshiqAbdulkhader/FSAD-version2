from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from config.database import query_db
from middleware.auth import token_required, get_current_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role', 'student')
        
        # Validation
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        if role not in ['student', 'staff', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Check if user already exists
        existing_user = query_db(
            'SELECT id FROM users WHERE email = %s',
            (email,),
            fetch_one=True
        )
        
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        query_db(
            'INSERT INTO users (email, password, name, role) VALUES (%s, %s, %s, %s)',
            (email, hashed_password, name, role)
        )
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get user from database
        user = query_db(
            'SELECT id, email, password, name, role FROM users WHERE email = %s',
            (email,),
            fetch_one=True
        )
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create JWT token (identity must be a string)
        access_token = create_access_token(identity=str(user[0]))
        
        return jsonify({
            'token': access_token,
            'user': {
                'id': user[0],
                'email': user[1],
                'name': user[3],
                'role': user[4]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET'])
@token_required
def get_me():
    """Get current user information"""
    user = get_current_user()
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

