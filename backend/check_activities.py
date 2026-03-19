import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.db import get_db
from datetime import datetime, timedelta
from bson import ObjectId
from models.activity import ActivityModel

db = get_db()
model = ActivityModel(db)

# Simulate what the API does - user_id as string
user_id = "694e43f6caf419b79fe5c93a"

with open('debug_output.txt', 'w') as f:
    f.write(f"Testing get_weekly_trends with user_id='{user_id}' (string)\n\n")
    
    trends = model.get_weekly_trends(user_id)
    
    for t in trends:
        f.write(f"  {t.get('date','?')} prod={t.get('productive_minutes',0)} dist={t.get('distracting_minutes',0)} total={t.get('total_minutes',0)}\n")
    
    f.write(f"\nTotal trends: {len(trends)}\n")
    f.write(f"Total data: {sum(t.get('total_minutes', 0) for t in trends)}\n")

print("Done!")
