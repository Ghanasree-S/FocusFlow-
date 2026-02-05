"""Test hourly breakdown after fix"""
import sys
sys.path.insert(0, '.')
from utils.db import get_db
from models.activity import ActivityModel

db = get_db()
uid = str(db.users.find_one({'email': 'ghanasreesk24@gmail.com'})['_id'])

model = ActivityModel(db)
hourly = model.get_hourly_breakdown(uid, days=7)

print("HOURLY BREAKDOWN (after fix):")
total_prod = 0
total_dist = 0
for h in hourly:
    prod = h.get('productive', 0)
    dist = h.get('distracted', 0)
    total_prod += prod
    total_dist += dist
    print(f"  {h.get('time')}: productive={prod:.0f}min, distracted={dist:.0f}min")

print(f"\nTOTAL: productive={total_prod:.0f}min, distracted={total_dist:.0f}min")
print(f"HOURS: productive={total_prod/60:.1f}h, distracted={total_dist/60:.1f}h")
