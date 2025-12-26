"""
User Model and Operations
"""
from datetime import datetime
from bson import ObjectId
import bcrypt

class UserModel:
    """User database operations"""
    
    def __init__(self, db):
        self.collection = db.users
    
    def create_user(self, name: str, email: str, password: str, style: str = 'Balanced', goals: list = None) -> dict:
        """Create a new user"""
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = {
            'name': name,
            'email': email.lower(),
            'password_hash': password_hash,
            'style': style,
            'goals': goals or [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user)
        user['_id'] = result.inserted_id
        return self._serialize(user)
    
    def find_by_email(self, email: str) -> dict:
        """Find user by email"""
        user = self.collection.find_one({'email': email.lower()})
        return user
    
    def find_by_id(self, user_id: str) -> dict:
        """Find user by ID"""
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        return self._serialize(user) if user else None
    
    def verify_password(self, user: dict, password: str) -> bool:
        """Verify user password"""
        return bcrypt.checkpw(password.encode('utf-8'), user['password_hash'])
    
    def update_profile(self, user_id: str, updates: dict) -> dict:
        """Update user profile"""
        allowed_fields = ['name', 'style', 'goals']
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}
        filtered_updates['updated_at'] = datetime.utcnow()
        
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': filtered_updates}
        )
        return self.find_by_id(user_id)
    
    def _serialize(self, user: dict) -> dict:
        """Serialize user for API response (exclude password)"""
        if not user:
            return None
        return {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'style': user.get('style', 'Balanced'),
            'goals': user.get('goals', []),
            'created_at': user.get('created_at', datetime.utcnow()).isoformat()
        }
