"""
Seed script to create demo user and initialize database collections
Creates only user - no mock data, tracker will collect real data
"""
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db import get_db
from models.user import UserModel

def seed_database():
    """Initialize database with demo user only"""
    print("=" * 50)
    print("🗃️  FocusFlow Database Setup")
    print("=" * 50)
    print()
    
    db = get_db()
    print("✅ Connected to MongoDB Atlas")
    
    # Create collections (MongoDB creates them automatically, but this ensures indexes)
    print()
    print("📂 Creating collections...")
    
    collections = ['users', 'tasks', 'activities', 'focus_sessions']
    for collection in collections:
        # Ensure collection exists by accessing it
        db[collection].find_one()
        print(f"   ✓ {collection}")
    
    # Create demo user
    print()
    print("👤 Creating demo user...")
    
    user_model = UserModel(db)
    existing_user = user_model.find_by_email('demo@focusflow.ai')
    
    if existing_user:
        print("   ℹ️  Demo user already exists")
        user_id = str(existing_user['_id'])
    else:
        user = user_model.create_user(
            name='Demo User',
            email='demo@focusflow.ai',
            password='demo123',
            style='Balanced',
            goals=['Improve focus', 'Track productivity', 'Reduce distractions']
        )
        user_id = user['id']
        print("   ✅ Demo user created")
    
    print()
    print("=" * 50)
    print("✅ DATABASE READY!")
    print("=" * 50)
    print()
    print("📋 Collections created:")
    print("   • users         - User accounts")
    print("   • tasks         - Task management")
    print("   • activities    - App usage tracking (real-time)")
    print("   • focus_sessions - Focus mode sessions")
    print()
    print("🔐 Demo Login Credentials:")
    print("   Email:    demo@focusflow.ai")
    print("   Password: demo123")
    print()
    print("🚀 Next step: Run 'python app.py' to start server + tracker")
    print("=" * 50)

if __name__ == '__main__':
    seed_database()
