"""
Insights and ML Prediction Routes
"""
from flask import Blueprint, request, jsonify
from utils.db import get_db
from utils.auth_middleware import token_required
from models.task import TaskModel
from models.activity import ActivityModel
from models.focus_session import FocusSessionModel
from ml.productivity_classifier import ProductivityClassifier
from ml.time_series_forecaster import TimeSeriesForecaster

insights_bp = Blueprint('insights', __name__, url_prefix='/api/insights')

@insights_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    """Get aggregated dashboard data"""
    db = get_db()
    user_id = request.current_user['id']
    
    task_model = TaskModel(db)
    activity_model = ActivityModel(db)
    focus_model = FocusSessionModel(db)
    
    # Get all stats
    task_stats = task_model.get_task_stats(user_id)
    focus_stats = focus_model.get_focus_stats(user_id)
    daily_summary = activity_model.get_daily_summary(user_id)
    hourly_data = activity_model.get_hourly_breakdown(user_id)
    
    # Calculate focus score from real data (0 if no data)
    total_time = daily_summary.get('total_minutes', 0)
    productive_time = daily_summary.get('productive_minutes', 0)
    focus_score = round((productive_time / total_time * 100) if total_time > 0 else 0)
    
    # Calculate distraction spikes from real data
    distracted_time = daily_summary.get('distracting_minutes', 0)
    distraction_spikes = min(10, distracted_time // 30) if distracted_time > 0 else 0
    
    return jsonify({
        'taskStats': task_stats,
        'focusStats': focus_stats,
        'dailySummary': daily_summary,
        'hourlyData': hourly_data,
        'focusScore': focus_score,
        'distractionSpikes': distraction_spikes,
        'hasData': total_time > 0
    })

@insights_bp.route('/forecast', methods=['GET'])
@token_required
def get_forecast():
    """Get ML-based productivity forecast"""
    db = get_db()
    user_id = request.current_user['id']
    
    try:
        # Get historical data
        activity_model = ActivityModel(db)
        task_model = TaskModel(db)
        focus_model = FocusSessionModel(db)
        
        # Gather features for prediction
        weekly_trends = activity_model.get_weekly_trends(user_id)
        task_stats = task_model.get_task_stats(user_id)
        focus_stats = focus_model.get_focus_stats(user_id)
        
        # Run ML predictions
        classifier = ProductivityClassifier()
        forecaster = TimeSeriesForecaster()
        
        # Classify current productivity level
        productivity_level = classifier.predict(weekly_trends, task_stats, focus_stats)
        
        # Forecast next 7 days
        forecast = forecaster.forecast(weekly_trends)
        
        return jsonify({
            'productivityLevel': productivity_level,
            'nextDayWorkload': forecast.get('next_day_workload', 75),
            'completionProbability': forecast.get('completion_probability', 82),
            'bestFocusWindow': forecast.get('best_focus_window', '09:00 AM - 11:30 AM'),
            'distractionTrigger': forecast.get('distraction_trigger', 'Social Media'),
            'trend': forecast.get('trend', 'Up'),
            'weeklyForecast': forecast.get('weekly_forecast', []),
            'expectedLoadLevel': forecast.get('load_level', 'Medium'),
            'stressRisk': forecast.get('stress_risk', 'Low')
        })
        
    except Exception as e:
        # Calculate real values from database even if ML fails
        try:
            activity_model = ActivityModel(db)
            task_model = TaskModel(db)
            focus_model = FocusSessionModel(db)
            
            weekly_trends = activity_model.get_weekly_trends(user_id)
            task_stats = task_model.get_task_stats(user_id)
            focus_stats = focus_model.get_focus_stats(user_id)
            hourly = activity_model.get_hourly_breakdown(user_id, 7)
            
            # Calculate real productivity level from data
            total_productive = sum(d.get('productive_minutes', 0) for d in weekly_trends)
            total_distracted = sum(d.get('distracting_minutes', 0) for d in weekly_trends)
            focus_ratio = total_productive / max(total_productive + total_distracted, 1)
            
            if focus_ratio >= 0.7:
                level = 'High'
            elif focus_ratio >= 0.4:
                level = 'Medium'
            else:
                level = 'Low'
            
            # Calculate workload from tasks
            pending_tasks = task_stats.get('total', 0) - task_stats.get('completed', 0)
            workload = min(100, pending_tasks * 15)
            
            # Find best focus window from real data
            best_window = '09:00 AM - 11:30 AM'
            if hourly:
                sorted_hours = sorted(hourly, key=lambda x: x.get('productive', 0), reverse=True)
                if sorted_hours and sorted_hours[0].get('productive', 0) > 0:
                    best_hour = sorted_hours[0]['time']
                    best_window = f"{best_hour} - {int(best_hour.split(':')[0]) + 2}:00"
            
            return jsonify({
                'productivityLevel': level,
                'nextDayWorkload': workload,
                'completionProbability': round(focus_ratio * 100),
                'bestFocusWindow': best_window,
                'distractionTrigger': 'Social Media',
                'trend': 'Up' if focus_ratio > 0.5 else 'Down',
                'weeklyForecast': [],
                'expectedLoadLevel': 'High' if pending_tasks > 5 else 'Medium' if pending_tasks > 2 else 'Low',
                'stressRisk': 'High' if pending_tasks > 7 else 'Medium' if pending_tasks > 3 else 'Low',
                'source': 'real_data',
                'debug': str(e)
            })
        except:
            # Only return error if even basic data fetch fails
            return jsonify({
                'productivityLevel': 'Unknown',
                'nextDayWorkload': 0,
                'completionProbability': 0,
                'bestFocusWindow': 'No data',
                'distractionTrigger': 'No data',
                'trend': 'Stable',
                'weeklyForecast': [],
                'expectedLoadLevel': 'Unknown',
                'stressRisk': 'Unknown',
                'error': 'No activity data available. Start the tracker to collect data.'
            })

@insights_bp.route('/trends', methods=['GET'])
@token_required
def get_trends():
    """Get time-series trend data"""
    db = get_db()
    user_id = request.current_user['id']
    
    activity_model = ActivityModel(db)
    focus_model = FocusSessionModel(db)
    
    days = request.args.get('days', 7, type=int)
    
    # Get weekly activity trends
    weekly_trends = activity_model.get_weekly_trends(user_id)
    hourly_breakdown = activity_model.get_hourly_breakdown(user_id, days)
    focus_stats = focus_model.get_focus_stats(user_id, days)
    
    return jsonify({
        'weeklyTrends': weekly_trends,
        'hourlyBreakdown': hourly_breakdown,
        'focusStats': focus_stats
    })

@insights_bp.route('/behavioral-patterns', methods=['GET'])
@token_required
def get_behavioral_patterns():
    """Get behavioral pattern insights"""
    db = get_db()
    user_id = request.current_user['id']
    
    activity_model = ActivityModel(db)
    focus_model = FocusSessionModel(db)
    
    # Get data for analysis
    weekly_trends = activity_model.get_weekly_trends(user_id)
    hourly = activity_model.get_hourly_breakdown(user_id, 14)  # 2 weeks
    focus_stats = focus_model.get_focus_stats(user_id, 14)
    
    # Analyze patterns
    patterns = _analyze_patterns(weekly_trends, hourly, focus_stats)
    
    return jsonify({'patterns': patterns})

@insights_bp.route('/reports/weekly', methods=['GET'])
@token_required
def get_weekly_report():
    """Generate weekly performance report"""
    db = get_db()
    user_id = request.current_user['id']
    
    task_model = TaskModel(db)
    activity_model = ActivityModel(db)
    focus_model = FocusSessionModel(db)
    
    # Gather weekly data
    task_stats = task_model.get_task_stats(user_id)
    weekly_trends = activity_model.get_weekly_trends(user_id)
    focus_stats = focus_model.get_focus_stats(user_id, 7)
    
    # Calculate metrics
    total_productive = sum(d['productive_minutes'] for d in weekly_trends)
    total_distracted = sum(d['distracting_minutes'] for d in weekly_trends)
    
    report = {
        'period': 'Last 7 days',
        'tasksCompleted': task_stats['completed'],
        'tasksCreated': task_stats['total'],
        'completionRate': round(task_stats['completed'] / task_stats['total'] * 100) if task_stats['total'] > 0 else 0,
        'totalFocusTime': f"{focus_stats['total_focus_time']:.0f} min",
        'avgSessionDuration': f"{focus_stats['avg_duration']:.1f} min",
        'productiveTime': f"{total_productive} min",
        'distractedTime': f"{total_distracted} min",
        'focusScore': round(total_productive / (total_productive + total_distracted) * 100) if (total_productive + total_distracted) > 0 else 85
    }
    
    return jsonify({'report': report})

def _analyze_patterns(weekly_trends, hourly, focus_stats):
    """Analyze user behavioral patterns"""
    patterns = []
    
    # Find most productive hour
    if hourly:
        productive_hours = sorted(hourly, key=lambda x: x['productive'], reverse=True)
        if productive_hours:
            best_hour = productive_hours[0]['time']
            patterns.append({
                'type': 'Optimization',
                'title': 'Peak Performance Hour',
                'description': f"Your most productive hour is around {best_hour}. Schedule important tasks during this time.",
                'icon': 'Lightbulb'
            })
    
    # Check consistency
    if weekly_trends:
        productive_days = sum(1 for d in weekly_trends if d['productive_minutes'] > 120)
        if productive_days >= 5:
            patterns.append({
                'type': 'Growth',
                'title': 'Consistency Streak',
                'description': f"You've been productive for {productive_days} out of 7 days. Keep up the great work!",
                'icon': 'Timer'
            })
    
    # Focus session insights
    if focus_stats.get('avg_duration', 0) > 45:
        patterns.append({
            'type': 'Growth',
            'title': 'Deep Work Capacity',
            'description': f"Your average focus session is {focus_stats['avg_duration']:.0f} minutes - excellent for deep work!",
            'icon': 'Timer'
        })
    
    # Distraction warning
    if hourly:
        distracted_hours = sorted(hourly, key=lambda x: x['distracted'], reverse=True)
        if distracted_hours and distracted_hours[0]['distracted'] > 30:
            patterns.append({
                'type': 'Warning',
                'title': 'Distraction Alert',
                'description': f"High distraction detected around {distracted_hours[0]['time']}. Consider blocking distracting apps.",
                'icon': 'ShieldAlert'
            })
    
    # Default pattern if none found
    if not patterns:
        patterns = [
            {
                'type': 'Optimization',
                'title': 'Getting Started',
                'description': 'Start logging your activities to get personalized insights!',
                'icon': 'Lightbulb'
            }
        ]
    
    return patterns
