"""Properly distribute activities across last 7 days"""
import sys
sys.path.insert(0, '.')
from utils.db import get_db
from datetime import datetime, timedelta
import random

db = get_db()
uid = str(db.users.find_one({'email': 'ghanasreesk24@gmail.com'})['_id'])

# Get all activities
activities = list(db.activities.find({'user_id': uid}))
print(f"Total activities: {len(activities)}")

# Distribute across last 7 days with realistic hours (8am - 10pm)
now = datetime.utcnow()

for i, act in enumerate(activities):
    # Random day in last 7 days (0=today, 6=7 days ago)
    days_ago = random.randint(0, 6)
    
    # Random hour between 8am and 10pm
    hour = random.randint(8, 22)
    minute = random.randint(0, 59)
    
    new_ts = now - timedelta(days=days_ago)
    new_ts = new_ts.replace(hour=hour, minute=minute, second=random.randint(0, 59))
    
    db.activities.update_one(
        {'_id': act['_id']},
        {'$set': {'timestamp': new_ts, 'created_at': new_ts}}
    )

print(f"Updated {len(activities)} activities")

# Verify
newest = db.activities.find_one({}, sort=[('timestamp', -1)])
oldest = db.activities.find_one({}, sort=[('timestamp', 1)])
print(f"Date range: {oldest.get('timestamp')} to {newest.get('timestamp')}")

# Check distribution
for d in range(7):
    start = now - timedelta(days=d+1)
    end = now - timedelta(days=d)
    count = db.activities.count_documents({
        'user_id': uid,
        'timestamp': {'$gte': start, '$lt': end}
    })
    print(f"  Day -{d}: {count} activities")
