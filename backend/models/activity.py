"""
Activity Model and Operations
"""
from datetime import datetime, timedelta
from bson import ObjectId

class ActivityModel:
    """Activity tracking database operations"""
    
    PRODUCTIVE_APPS = ['vscode', 'code', 'terminal', 'word', 'excel', 'powerpoint', 
                        'notion', 'slack', 'teams', 'zoom', 'figma', 'photoshop']
    DISTRACTING_APPS = ['youtube', 'netflix', 'twitter', 'facebook', 'instagram', 
                         'tiktok', 'reddit', 'twitch', 'games']
    
    def __init__(self, db):
        self.collection = db.activities
    
    def log_activity(self, user_id: str, app_name: str, duration_minutes: int, 
                     category: str = None, timestamp: datetime = None) -> dict:
        """Log an activity"""
        app_lower = app_name.lower()
        
        # Auto-categorize if not provided
        if category is None:
            if any(prod in app_lower for prod in self.PRODUCTIVE_APPS):
                category = 'productive'
            elif any(dist in app_lower for dist in self.DISTRACTING_APPS):
                category = 'distracting'
            else:
                category = 'neutral'
        
        activity = {
            'user_id': user_id,
            'app_name': app_name,
            'category': category,
            'duration_minutes': duration_minutes,
            'is_productive': category == 'productive',
            'timestamp': timestamp or datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(activity)
        activity['_id'] = result.inserted_id
        return self._serialize(activity)
    
    def get_activities(self, user_id: str, days: int = 7) -> list:
        """Get activities for the last N days"""
        from bson import ObjectId
        
        # Convert to ObjectId if string
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        activities = self.collection.find({
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }).sort('timestamp', -1)
        
        return [self._serialize(act) for act in activities]
    
    def get_daily_summary(self, user_id: str, date: datetime = None) -> dict:
        """Get activity summary for a specific day"""
        from bson import ObjectId
        
        # Convert to ObjectId if string
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        
        if date is None:
            date = datetime.utcnow()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        pipeline = [
            {'$match': {
                'user_id': user_id,
                'timestamp': {'$gte': start_of_day, '$lt': end_of_day}
            }},
            {'$group': {
                '_id': '$category',
                'total_minutes': {'$sum': '$duration_minutes'},
                'count': {'$sum': 1}
            }}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        summary = {
            'date': start_of_day.strftime('%Y-%m-%d'),
            'productive_minutes': 0,
            'distracting_minutes': 0,
            'neutral_minutes': 0,
            'total_minutes': 0
        }
        
        for r in results:
            if r['_id'] == 'productive':
                summary['productive_minutes'] = r['total_minutes']
            elif r['_id'] == 'distracting':
                summary['distracting_minutes'] = r['total_minutes']
            else:
                summary['neutral_minutes'] = r['total_minutes']
        
        summary['total_minutes'] = (summary['productive_minutes'] + 
                                     summary['distracting_minutes'] + 
                                     summary['neutral_minutes'])
        
        return summary
    
    def get_weekly_trends(self, user_id: str) -> list:
        """Get weekly activity trends"""
        trends = []
        for i in range(7):
            date = datetime.utcnow() - timedelta(days=i)
            summary = self.get_daily_summary(user_id, date)
            trends.append(summary)
        
        return list(reversed(trends))
    
    def get_hourly_breakdown(self, user_id: str, days: int = 7) -> list:
        """Get hourly activity breakdown"""
        from bson import ObjectId
        
        # Convert to ObjectId if string
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {'$match': {
                'user_id': user_id,
                'timestamp': {'$gte': start_date}
            }},
            {'$group': {
                '_id': {'$hour': '$timestamp'},
                'productive': {'$sum': {'$cond': ['$is_productive', '$duration_minutes', 0]}},
                'distracted': {'$sum': {'$cond': ['$is_productive', 0, '$duration_minutes']}}
            }},
            {'$sort': {'_id': 1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # Format for frontend chart
        hourly = []
        for r in results:
            hour = r['_id']
            hourly.append({
                'time': f'{hour:02d}:00',
                'productive': r['productive'],
                'distracted': r['distracted']
            })
        
        return hourly
    
    def get_top_apps(self, user_id: str, days: int = 7, category: str = None) -> list:
        """Get top apps by duration, optionally filtered by category"""
        from bson import ObjectId
        
        # Convert to ObjectId if string
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        match_stage = {
            'user_id': user_id,
            'timestamp': {'$gte': start_date}
        }
        
        if category:
            match_stage['category'] = category
        
        pipeline = [
            {'$match': match_stage},
            {'$group': {
                '_id': '$app_name',
                'total_minutes': {'$sum': '$duration_minutes'},
                'count': {'$sum': 1}
            }},
            {'$sort': {'total_minutes': -1}},
            {'$limit': 10}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        return [
            {
                'app_name': r['_id'],
                'total_minutes': r['total_minutes'],
                'count': r['count']
            }
            for r in results
        ]
    
    def _serialize(self, activity: dict) -> dict:
        """Serialize activity for API response"""
        if not activity:
            return None
        
        # Handle missing is_productive field (for older records)
        is_productive = activity.get('is_productive')
        if is_productive is None:
            # Derive from category if is_productive field is missing
            category = activity.get('category', 'neutral')
            is_productive = category == 'productive'
        
        return {
            'id': str(activity['_id']),
            'app_name': activity.get('app_name', 'Unknown'),
            'category': activity.get('category', 'neutral'),
            'duration_minutes': activity.get('duration_minutes', 0),
            'is_productive': is_productive,
            'timestamp': activity.get('timestamp', datetime.utcnow()).isoformat()
        }
