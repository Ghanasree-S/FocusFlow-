"""Test analytics after timestamp fix"""
import sys
sys.path.insert(0, '.')
from utils.db import get_db
from models.activity import ActivityModel

db = get_db()
user = db.users.find_one({'email': 'ghanasreesk24@gmail.com'})
user_id = str(user['_id'])

model = ActivityModel(db)

# Test weekly trends
trends = model.get_weekly_trends(user_id)
print('Weekly Trends:')
for t in trends:
    print(f"  {t.get('date')}: prod={t.get('productive_minutes')}, dist={t.get('distracting_minutes')}, total={t.get('total_minutes')}")

# Test hourly breakdown
hourly = model.get_hourly_breakdown(user_id, days=7)
print(f'\nHourly breakdown: {len(hourly)} hours with data')
for h in hourly[:5]:
    print(f"  {h.get('time')}: prod={h.get('productive')}, dist={h.get('distracted')}")

# Test top apps
top = model.get_top_apps(user_id, days=7)
print(f'\nTop apps: {len(top)} apps')
for a in top[:5]:
    print(f"  {a.get('app_name')}: {a.get('total_minutes')}min")
