"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config
from utils.db import get_db
from utils.auth_middleware import token_required
from models.user import UserModel

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'email', 'password']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields: name, email, password'}), 400
    
    db = get_db()
    user_model = UserModel(db)
    
    # Check if email already exists
    if user_model.find_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    try:
        user = user_model.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            style=data.get('style', 'Balanced'),
            goals=data.get('goals', [])
        )
        
        # Generate JWT token
        token = _generate_token(user['id'])
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    db = get_db()
    user_model = UserModel(db)
    
    # Find user
    user = user_model.find_by_email(data['email'])
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Verify password
    if not user_model.verify_password(user, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate token
    token = _generate_token(str(user['_id']))
    
    return jsonify({
        'message': 'Login successful',
        'user': user_model._serialize(user),
        'token': token
    })

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    db = get_db()
    user_model = UserModel(db)
    
    user = user_model.find_by_id(request.current_user['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user})

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    data = request.get_json()
    
    db = get_db()
    user_model = UserModel(db)
    
    user = user_model.update_profile(request.current_user['id'], data)
    if not user:
        return jsonify({'error': 'Failed to update profile'}), 400
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user
    })

def _generate_token(user_id: str) -> str:
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')
