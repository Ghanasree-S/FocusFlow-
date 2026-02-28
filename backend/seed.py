"""
Seed script to create demo user, initialize database collections, and add sample data
"""
import os
import sys
import random
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db import get_db
from models.user import UserModel

def seed_database():
    """Initialize database with demo user only"""
    print("=" * 50)
    print("ðŸ—ƒï¸  ChronosAI Database Setup")
    print("=" * 50)
    print()
    
    db = get_db()
    print("âœ… Connected to MongoDB Atlas")
    
    # Create collections (MongoDB creates them automatically, but this ensures indexes)
    print()
    print("ðŸ“‚ Creating collections...")
    
    collections = ['users', 'tasks', 'activities', 'focus_sessions']
    for collection in collections:
        # Ensure collection exists by accessing it
        db[collection].find_one()
        print(f"   âœ“ {collection}")
    
    # Create demo user
    print()
    print("ðŸ‘¤ Creating demo user...")
    
    user_model = UserModel(db)
    existing_user = user_model.find_by_email('demo@ChronosAI.ai')
    
    if existing_user:
        print("   â„¹ï¸  Demo user already exists")
        user_id = str(existing_user['_id'])
    else:
        user = user_model.create_user(
            name='Demo User',
            email='demo@ChronosAI.ai',
            password='demo123',
            style='Balanced',
            goals=['Improve focus', 'Track productivity', 'Reduce distractions']
        )
        user_id = user['id']
        print("   âœ… Demo user created")
    
    print()
    print("=" * 50)
    print("âœ… DATABASE READY!")
    print("=" * 50)
    print()
    print("ðŸ“‹ Collections created:")
    print("   â€¢ users         - User accounts")
    print("   â€¢ tasks         - Task management")
    print("   â€¢ activities    - App usage tracking (real-time)")
    print("   â€¢ focus_sessions - Focus mode sessions")
    print()
    print("ðŸ” Demo Login Credentials:")
    print("   Email:    demo@ChronosAI.ai")
    print("   Password: demo123")
    print()
    
    # Add sample activity data for demo user
    seed_activities(db, user_id)
    
    # Add sample data for ALL other users too
    print("ðŸ“Š Adding data for all users...")
    all_users = db.users.find({})
    for u in all_users:
        if str(u['_id']) != user_id:
            seed_activities(db, u['_id'])
    
    print("ðŸš€ Next step: Run 'python app.py' to start server")
    print("=" * 50)


def seed_activities(db, user_id):
    """Add sample activity data for the past 7 days"""
    from bson import ObjectId
    
    print("ðŸ“Š Adding sample activity data...")
    
    # Convert user_id to ObjectId if needed
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    # Clear existing activities
    db.activities.delete_many({'user_id': user_id})
    db.focus_sessions.delete_many({'user_id': user_id})
    
    # Apps to simulate
    productive_apps = ['Visual Studio Code', 'GitHub', 'ChatGPT', 'Google Docs', 'Stack Overflow', 'Figma', 'Notion']
    distracting_apps = ['YouTube', 'Netflix', 'Reddit', 'Instagram', 'Twitter', 'Facebook']
    neutral_apps = ['Gmail', 'Google Search', 'News', 'Weather']
    
    activities = []
    focus_sessions = []
    
    # Generate data for the past 7 days
    for day_offset in range(7):
        current_date = datetime.utcnow() - timedelta(days=day_offset)
        
        # Morning - mostly productive
        for _ in range(random.randint(4, 6)):
            app = random.choice(productive_apps)
            activities.append({
                'user_id': user_id,
                'app_name': app,
                'duration_minutes': random.randint(10, 45),
                'category': 'productive',
                'is_productive': True,
                'timestamp': current_date.replace(hour=random.randint(9, 11), minute=random.randint(0, 59)),
                'created_at': current_date
            })
        
        # Afternoon - mixed
        for _ in range(random.randint(3, 5)):
            if random.random() < 0.6:
                app, category = random.choice(productive_apps), 'productive'
            elif random.random() < 0.8:
                app, category = random.choice(neutral_apps), 'neutral'
            else:
                app, category = random.choice(distracting_apps), 'distracting'
            
            activities.append({
                'user_id': user_id,
                'app_name': app,
                'duration_minutes': random.randint(5, 30),
                'category': category,
                'is_productive': category == 'productive',
                'timestamp': current_date.replace(hour=random.randint(14, 16), minute=random.randint(0, 59)),
                'created_at': current_date
            })
        
        # Evening - more distractions
        for _ in range(random.randint(2, 4)):
            if random.random() < 0.3:
                app, category = random.choice(productive_apps), 'productive'
            else:
                app, category = random.choice(distracting_apps), 'distracting'
            
            activities.append({
                'user_id': user_id,
                'app_name': app,
                'duration_minutes': random.randint(10, 60),
                'category': category,
                'is_productive': category == 'productive',
                'timestamp': current_date.replace(hour=random.randint(18, 20), minute=random.randint(0, 59)),
                'created_at': current_date
            })
        
        # Add focus sessions
        for _ in range(random.randint(2, 3)):
            start = current_date.replace(hour=random.randint(9, 17), minute=random.randint(0, 59))
            planned = random.choice([15, 25, 30, 45])
            completed = random.random() < 0.8
            actual = planned if completed else random.randint(5, planned - 1)
            focus_sessions.append({
                'user_id': user_id,
                'planned_duration': planned,
                'actual_duration': actual,
                'completed': completed,
                'start_time': start,
                'end_time': start + timedelta(minutes=actual),
                'created_at': start
            })
    
    # Insert all data
    if activities:
        db.activities.insert_many(activities)
        print(f"   âœ… Added {len(activities)} activities (7 days)")
    
    if focus_sessions:
        db.focus_sessions.insert_many(focus_sessions)
        print(f"   âœ… Added {len(focus_sessions)} focus sessions")
    
    print()


if __name__ == '__main__':
    seed_database()
