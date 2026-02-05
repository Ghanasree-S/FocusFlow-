"""Fix all activities to belong to Ghanasree"""
import sys
sys.path.insert(0, '.')
from utils.db import get_db
from bson import ObjectId

db = get_db()

# Get Ghanasree's user ID
ghanasree = db.users.find_one({'email': 'ghanasreesk24@gmail.com'})
ghanasree_id = str(ghanasree['_id'])

print(f'Ghanasree ID: {ghanasree_id}')

# Count current activities
total = db.activities.count_documents({})
print(f'Total activities: {total}')

# Update all activities to belong to Ghanasree
result = db.activities.update_many({}, {'$set': {'user_id': ghanasree_id}})
print(f'Updated {result.modified_count} activities to Ghanasree')

# Also update focus sessions
result2 = db.focus_sessions.update_many({}, {'$set': {'user_id': ghanasree_id}})
print(f'Updated {result2.modified_count} focus sessions to Ghanasree')

# Verify
final = db.activities.count_documents({'user_id': ghanasree_id})
print(f'Final Ghanasree activities: {final}')
