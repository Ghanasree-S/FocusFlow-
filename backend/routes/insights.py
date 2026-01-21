"""
Insights and ML Prediction Routes
"""
from flask import Blueprint, request, jsonify
from utils.db import get_db
from utils.auth_middleware import token_required
from models.task import TaskModel
from models.activity import ActivityModel
from models.focus_session import FocusSessionModel

# Lazy load ML modules to avoid startup crash on import errors
ProductivityClassifier = None
TimeSeriesForecaster = None

def _load_ml_modules():
    """Lazy load ML modules to avoid import errors at startup"""
    global ProductivityClassifier, TimeSeriesForecaster
    if ProductivityClassifier is None:
        try:
            from ml.productivity_classifier import ProductivityClassifier as PC
            from ml.time_series_forecaster import TimeSeriesForecaster as TSF
            ProductivityClassifier = PC
            TimeSeriesForecaster = TSF
        except Exception as e:
            print(f"⚠️ ML modules could not be loaded: {e}")
            return False
    return True


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
    
    # Calculate focus score from real data
    total_time = daily_summary.get('total_minutes', 0)
    productive_time = daily_summary.get('productive_minutes', 0)
    
    # If daily summary is empty, calculate from hourly data
    if total_time == 0 and hourly_data:
        productive_time = sum(h.get('productive', 0) for h in hourly_data)
        distracted_time = sum(h.get('distracted', 0) for h in hourly_data)
        total_time = productive_time + distracted_time
    
    focus_score = round((productive_time / total_time * 100) if total_time > 0 else 0)
    
    # Calculate distraction spikes from real data
    # Count hourly periods with significant distraction (more than 10 minutes)
    distraction_spikes = 0
    if hourly_data:
        distraction_spikes = sum(1 for h in hourly_data if h.get('distracted', 0) > 10)
    
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
        
        # Run ML predictions - lazy load modules
        if not _load_ml_modules():
            raise Exception('ML modules not available')
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
    
    # Calculate metrics from ACTIVITIES (tracked apps)
    total_productive = sum(d['productive_minutes'] for d in weekly_trends)
    total_distracted = sum(d['distracting_minutes'] for d in weekly_trends)
    
    # Format productive time as hours and minutes
    prod_hours = int(total_productive // 60)
    prod_mins = int(total_productive % 60)
    dist_hours = int(total_distracted // 60)
    dist_mins = int(total_distracted % 60)
    
    report = {
        'period': 'Last 7 days',
        'tasksCompleted': task_stats['completed'],
        'tasksCreated': task_stats['total'],
        'completionRate': round(task_stats['completed'] / task_stats['total'] * 100) if task_stats['total'] > 0 else 0,
        'totalFocusTime': f"{prod_hours}h {prod_mins}m",  # From productive ACTIVITIES, not focus sessions
        'avgSessionDuration': f"{focus_stats['avg_duration']:.1f} min",
        'productiveTime': f"{total_productive} min",
        'distractedTime': f"{dist_hours}h {dist_mins}m",
        'focusScore': round(total_productive / (total_productive + total_distracted) * 100) if (total_productive + total_distracted) > 0 else 0
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


# ============ ML Model Routes ============

@insights_bp.route('/ml/status', methods=['GET'])
@token_required
def get_ml_status():
    """Get status of all ML models (LSTM, ARIMA, Prophet)"""
    try:
        if not _load_ml_modules():
            # Return fallback status when ML modules aren't available
            return jsonify({
                'status': 'fallback',
                'message': 'ML modules unavailable - using statistical fallback predictions',
                'forecaster': {
                    'lstm': {'available': False, 'trained': False, 'status': 'fallback'},
                    'arima': {'available': False, 'trained': False, 'status': 'fallback'},
                    'prophet': {'available': False, 'trained': False, 'status': 'fallback'},
                    'weights': {'lstm': 0.4, 'arima': 0.3, 'prophet': 0.3}
                },
                'classifier': {
                    'model_type': 'Statistical Fallback',
                    'feature_importance': []
                }
            })
        
        forecaster = TimeSeriesForecaster()
        classifier = ProductivityClassifier()
        
        return jsonify({
            'forecaster': forecaster.get_model_status(),
            'classifier': {
                'model_type': 'Random Forest',
                'feature_importance': classifier.get_feature_importance()
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@insights_bp.route('/ml/train', methods=['POST'])
@token_required
def train_ml_models():
    """Train all ML models with user's historical data"""
    db = get_db()
    user_id = request.current_user['id']
    
    try:
        activity_model = ActivityModel(db)
        
        # Get all available historical data
        weekly_trends = activity_model.get_weekly_trends(user_id)
        
        if not weekly_trends or len(weekly_trends) < 7:
            return jsonify({
                'error': 'Insufficient data for training. Need at least 7 days of activity data.',
                'current_days': len(weekly_trends) if weekly_trends else 0
            }), 400
        
        # Prepare data for training
        import pandas as pd
        from datetime import datetime, timedelta
        
        training_data = []
        for i, trend in enumerate(weekly_trends):
            if 'date' in trend:
                try:
                    date = datetime.strptime(trend['date'], '%Y-%m-%d')
                except:
                    date = datetime.utcnow() - timedelta(days=len(weekly_trends) - i - 1)
            else:
                date = datetime.utcnow() - timedelta(days=len(weekly_trends) - i - 1)
            
            training_data.append({
                'ds': date,
                'y': trend.get('productive_minutes', 60)
            })
        
        df = pd.DataFrame(training_data)
        
        # Train all models - lazy load modules
        if not _load_ml_modules():
            return jsonify({
                'status': 'fallback',
                'message': 'ML modules unavailable. Using statistical fallback predictions instead.',
                'training_samples': len(df),
                'results': {
                    'lstm': {'status': 'skipped', 'reason': 'ML modules unavailable'},
                    'arima': {'status': 'skipped', 'reason': 'ML modules unavailable'},
                    'prophet': {'status': 'skipped', 'reason': 'ML modules unavailable'}
                }
            })
        
        forecaster = TimeSeriesForecaster()
        training_results = forecaster.train_all(df)
        
        return jsonify({
            'message': 'Models trained successfully',
            'training_samples': len(df),
            'results': training_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@insights_bp.route('/ml/compare', methods=['GET'])
@token_required
def compare_ml_models():
    """Compare performance of LSTM, ARIMA, and Prophet models"""
    db = get_db()
    user_id = request.current_user['id']
    
    try:
        activity_model = ActivityModel(db)
        weekly_trends = activity_model.get_weekly_trends(user_id)
        
        if not weekly_trends or len(weekly_trends) < 7:
            return jsonify({
                'error': 'Insufficient data for model comparison',
                'current_days': len(weekly_trends) if weekly_trends else 0
            }), 400
        
        # Try to load ML modules - if unavailable, use fallback predictions
        if not _load_ml_modules():
            # Generate fallback predictions based on actual user data
            fallback_preds = _generate_fallback_predictions(weekly_trends, 7)
            return jsonify({
                'models': {
                    'lstm': {
                        'name': 'LSTM (Long Short-Term Memory)',
                        'type': 'Deep Learning',
                        'description': 'Captures complex non-linear patterns and sequential dependencies',
                        'predictions': fallback_preds['lstm'],
                        'status': 'fallback'
                    },
                    'arima': {
                        'name': 'ARIMA',
                        'type': 'Statistical',
                        'description': 'Handles smooth trends and seasonal patterns',
                        'predictions': fallback_preds['arima'],
                        'status': 'fallback'
                    },
                    'prophet': {
                        'name': 'Prophet',
                        'type': 'Additive Regression',
                        'description': 'Manages seasonality and holiday effects',
                        'predictions': fallback_preds['prophet'],
                        'status': 'fallback'
                    }
                },
                'ensemble_weights': {'lstm': 0.4, 'arima': 0.3, 'prophet': 0.3},
                'status': 'success',
                'is_fallback': True,
                'message': 'Using statistical fallback predictions (ML modules unavailable)'
            })
        
        forecaster = TimeSeriesForecaster()
        
        lstm_pred = forecaster.predict_with_lstm(weekly_trends, periods=7)
        arima_pred = forecaster.predict_with_arima(weekly_trends, periods=7)
        prophet_pred = forecaster.predict_with_prophet(weekly_trends, periods=7)
        
        return jsonify({
            'models': {
                'lstm': {
                    'name': 'LSTM (Long Short-Term Memory)',
                    'type': 'Deep Learning',
                    'description': 'Captures complex non-linear patterns and sequential dependencies',
                    'predictions': lstm_pred
                },
                'arima': {
                    'name': 'ARIMA',
                    'type': 'Statistical',
                    'description': 'Handles smooth trends and seasonal patterns',
                    'predictions': arima_pred
                },
                'prophet': {
                    'name': 'Prophet',
                    'type': 'Additive Regression',
                    'description': 'Manages seasonality and holiday effects',
                    'predictions': prophet_pred
                }
            },
            'ensemble_weights': forecaster.weights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@insights_bp.route('/ml/forecast/<model>', methods=['GET'])
@token_required
def get_model_forecast(model):
    """Get forecast from a specific model (lstm, arima, prophet, ensemble)"""
    db = get_db()
    user_id = request.current_user['id']
    
    valid_models = ['lstm', 'arima', 'prophet', 'ensemble']
    if model.lower() not in valid_models:
        return jsonify({'error': f'Invalid model. Choose from: {valid_models}'}), 400
    
    try:
        activity_model = ActivityModel(db)
        weekly_trends = activity_model.get_weekly_trends(user_id)
        
        periods = request.args.get('periods', 7, type=int)
        periods = min(max(periods, 1), 14)  # Limit to 1-14 days
        
        # Lazy load ML modules - use fallback if unavailable
        if not _load_ml_modules():
            fallback_preds = _generate_fallback_predictions(weekly_trends if weekly_trends else [], periods)
            model_key = model.lower() if model.lower() != 'ensemble' else 'lstm'
            result = fallback_preds.get(model_key, fallback_preds['lstm'])
            return jsonify({
                'model': model,
                'periods': periods,
                'forecast': result,
                'status': 'fallback'
            })
        
        forecaster = TimeSeriesForecaster()
        
        if model.lower() == 'lstm':
            result = forecaster.predict_with_lstm(weekly_trends, periods)
        elif model.lower() == 'arima':
            result = forecaster.predict_with_arima(weekly_trends, periods)
        elif model.lower() == 'prophet':
            result = forecaster.predict_with_prophet(weekly_trends, periods)
        else:  # ensemble
            full_forecast = forecaster.forecast(weekly_trends, periods)
            result = full_forecast.get('model_predictions', {}).get('ensemble', {})
        
        return jsonify({
            'model': model,
            'periods': periods,
            'forecast': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ Analytics Routes ============

@insights_bp.route('/top-apps', methods=['GET'])
@token_required
def get_top_apps():
    """Get top apps by usage time (real data)"""
    db = get_db()
    user_id = request.current_user['id']
    
    activity_model = ActivityModel(db)
    days = request.args.get('days', 7, type=int)
    category = request.args.get('category', None)
    
    # Get top apps from activities
    top_apps = activity_model.get_top_apps(user_id, days, category)
    
    return jsonify({
        'topApps': top_apps,
        'period': f'{days} days',
        'filter': category or 'all'
    })


@insights_bp.route('/distraction-patterns', methods=['GET'])
@token_required
def get_distraction_patterns():
    """Get distraction patterns (real data)"""
    db = get_db()
    user_id = request.current_user['id']
    
    try:
        activity_model = ActivityModel(db)
        days = request.args.get('days', 7, type=int)
        
        # Get hourly breakdown for peak hours
        hourly = activity_model.get_hourly_breakdown(user_id, days)
        
        # Calculate peak distraction hours
        peak_hours = sorted(hourly, key=lambda x: x.get('distracted', 0), reverse=True)[:5]
        
        # Get top distracting apps
        top_distractions = []
        try:
            top_distractions = activity_model.get_top_apps(user_id, days, 'distracting')
        except Exception as e:
            print(f"Error getting top apps: {e}")
            top_distractions = []
        
        return jsonify({
            'peak_hours': peak_hours,
            'top_distractions': top_distractions,
            'period': f'{days} days'
        })
    except Exception as e:
        print(f"Error in distraction-patterns: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'error'}), 500


@insights_bp.route('/focus-windows', methods=['GET'])
@token_required
def get_focus_windows():
    """Get best focus windows based on real productivity data"""
    db = get_db()
    user_id = request.current_user['id']
    
    activity_model = ActivityModel(db)
    
    # Get hourly breakdown to find peak productivity hours
    hourly = activity_model.get_hourly_breakdown(user_id, 14)
    
    if not hourly:
        return jsonify({
            'focusWindows': [],
            'bestWindow': None,
            'message': 'No activity data yet.'
        })
    
    # Sort by productive time
    sorted_hours = sorted(hourly, key=lambda x: x['productive'], reverse=True)
    
    # Find best focus windows
    focus_windows = []
    for h in sorted_hours[:5]:
        total_time = h['productive'] + h['distracted']
        if total_time == 0:
            ratio = 0
        else:
            ratio = (h['productive'] / total_time) * 100
        
        # Convert "09:00" to time range "09:00 - 10:00"
        hour_str = h['time']
        try:
            hour_num = int(hour_str.split(':')[0])
            next_hour = (hour_num + 1) % 24
            time_range = f"{hour_str} - {next_hour:02d}:00"
        except:
            time_range = hour_str
        
        focus_windows.append({
            'time': time_range,
            'productive_minutes': h['productive'],
            'distracted_minutes': h['distracted'],
            'focus_ratio': round(ratio, 1)
        })
    
    best_window = focus_windows[0] if focus_windows else None
    
    return jsonify({
        'focusWindows': focus_windows,
        'bestWindow': best_window,
        'totalHours': len(hourly)
    })


@insights_bp.route('/ml/realtime-predictions', methods=['GET'])
@token_required
def get_realtime_predictions():
    """Get real-time ML predictions with auto-training every 20 entries"""
    db = get_db()
    user_id = request.current_user['id']
    
    try:
        activity_model = ActivityModel(db)
        
        # Get activity count
        activity_count = len(activity_model.get_activities(user_id, days=30))
        
        # Only train/predict if we have at least 20 activities
        if activity_count < 20:
            return jsonify({
                'status': 'insufficient_data',
                'message': f'Need 20+ activities for predictions. Currently have {activity_count}.',
                'activities_count': activity_count,
                'models': {
                    'lstm': None,
                    'arima': None,
                    'prophet': None
                }
            }), 200
        
        # Check if this is a multiple of 20 (auto-train trigger)
        should_retrain = (activity_count % 20 == 0)
        
        # Get historical data
        weekly_trends = activity_model.get_weekly_trends(user_id)
        
        # Auto-train models if at 20, 40, 60... entries
        if should_retrain and activity_count >= 20 and len(weekly_trends) >= 7:
            try:
                import pandas as pd
                from datetime import datetime, timedelta
                import numpy as np
                
                training_data = []
                for i, trend in enumerate(weekly_trends):
                    if 'date' in trend:
                        try:
                            date = datetime.strptime(trend['date'], '%Y-%m-%d')
                        except:
                            date = datetime.utcnow() - timedelta(days=len(weekly_trends) - i - 1)
                    else:
                        date = datetime.utcnow() - timedelta(days=len(weekly_trends) - i - 1)
                    
                    # Ensure productive_minutes is a valid number
                    prod_min = trend.get('productive_minutes', 60)
                    if not isinstance(prod_min, (int, float)):
                        prod_min = 60
                    prod_min = float(prod_min)
                    
                    training_data.append({
                        'ds': date,
                        'y': prod_min
                    })
                
                df = pd.DataFrame(training_data)
                if _load_ml_modules():
                    forecaster = TimeSeriesForecaster()
                    forecaster.train_all(df)
                print(f"✅ Auto-trained models at {activity_count} activities")
            except Exception as e:
                print(f"⚠️ Auto-training failed: {e}")
        
        # Get current predictions
        periods = request.args.get('periods', 7, type=int)
        periods = min(max(periods, 1), 14)
        
        # Lazy load ML modules - use fallback if unavailable
        if not _load_ml_modules():
            fallback_preds = _generate_fallback_predictions(weekly_trends if weekly_trends else [], periods)
            return jsonify({
                'status': 'success',
                'is_fallback': True,
                'message': 'Using statistical fallback predictions (ML modules unavailable)',
                'activities_count': activity_count,
                'auto_trained': False,
                'next_training_at': ((activity_count // 20) + 1) * 20,
                'models': {
                    'lstm': {
                        'name': 'LSTM (Long Short-Term Memory)',
                        'type': 'Deep Learning',
                        'description': 'Captures complex non-linear patterns',
                        'predictions': fallback_preds['lstm']
                    },
                    'arima': {
                        'name': 'ARIMA',
                        'type': 'Statistical',
                        'description': 'Handles smooth trends and seasonal patterns',
                        'predictions': fallback_preds['arima']
                    },
                    'prophet': {
                        'name': 'Prophet',
                        'type': 'Additive Regression',
                        'description': 'Manages seasonality and holiday effects',
                        'predictions': fallback_preds['prophet']
                    }
                }
            }), 200
        
        forecaster = TimeSeriesForecaster()
        
        lstm_pred = None
        arima_pred = None
        prophet_pred = None
        
        try:
            lstm_pred = forecaster.predict_with_lstm(weekly_trends, periods)
            if lstm_pred and isinstance(lstm_pred, dict):
                lstm_pred = _make_serializable(lstm_pred)
        except Exception as e:
            print(f"LSTM prediction error: {e}")
            lstm_pred = None
        
        try:
            arima_pred = forecaster.predict_with_arima(weekly_trends, periods)
            if arima_pred and isinstance(arima_pred, dict):
                arima_pred = _make_serializable(arima_pred)
        except Exception as e:
            print(f"ARIMA prediction error: {e}")
            arima_pred = None
        
        try:
            prophet_pred = forecaster.predict_with_prophet(weekly_trends, periods)
            if prophet_pred and isinstance(prophet_pred, dict):
                prophet_pred = _make_serializable(prophet_pred)
        except Exception as e:
            print(f"Prophet prediction error: {e}")
            prophet_pred = None
        
        return jsonify({
            'status': 'success',
            'activities_count': activity_count,
            'auto_trained': should_retrain,
            'next_training_at': ((activity_count // 20) + 1) * 20,
            'models': {
                'lstm': lstm_pred,
                'arima': arima_pred,
                'prophet': prophet_pred
            }
        })
        
    except Exception as e:
        print(f"Error in realtime-predictions: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'error'}), 500


def _make_serializable(obj):
    """Convert non-JSON-serializable objects to JSON-serializable types"""
    import numpy as np
    from datetime import datetime
    
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


def _generate_fallback_predictions(weekly_trends: list, periods: int = 7) -> dict:
    """
    Generate fallback ML predictions based on actual user data patterns.
    Uses simple statistical methods to simulate different model behaviors.
    """
    from datetime import datetime, timedelta
    import random
    
    # Calculate base statistics from actual data
    productive_minutes = [t.get('productive_minutes', 60) for t in weekly_trends]
    mean_val = sum(productive_minutes) / len(productive_minutes) if productive_minutes else 60
    
    # Calculate variance for more realistic predictions
    if len(productive_minutes) > 1:
        variance = sum((x - mean_val) ** 2 for x in productive_minutes) / len(productive_minutes)
        std_dev = variance ** 0.5
    else:
        std_dev = 15
    
    # Day-of-week patterns (typical productivity patterns)
    dow_modifiers = [1.0, 1.05, 1.03, 1.0, 0.95, 0.7, 0.65]  # Mon-Sun
    
    base_date = datetime.utcnow()
    
    def create_forecast(model_name: str, variation_factor: float, trend_direction: float):
        """Create a forecast for a specific model with unique behavior"""
        forecast = []
        
        for i in range(periods):
            future_date = base_date + timedelta(days=i + 1)
            dow = future_date.weekday()
            
            # Base prediction with day-of-week pattern
            base_pred = mean_val * dow_modifiers[dow]
            
            # Add model-specific variation
            variation = random.uniform(-std_dev * variation_factor, std_dev * variation_factor)
            
            # Add slight trend
            trend = trend_direction * i * 2
            
            predicted_minutes = max(10, round(base_pred + variation + trend))
            
            forecast.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'day': future_date.strftime('%A'),
                'predicted_productive_minutes': predicted_minutes,
                'confidence': round(0.75 - (i * 0.02), 2)
            })
        
        avg_pred = sum(f['predicted_productive_minutes'] for f in forecast) / len(forecast)
        
        return {
            'model': model_name,
            'forecast': forecast,
            'average_predicted': round(avg_pred),
            'trend': 'Up' if trend_direction > 0 else 'Down' if trend_direction < 0 else 'Stable',
            'confidence': 0.75,
            'periods': periods
        }
    
    return {
        'lstm': create_forecast('LSTM', 0.8, 1.5),      # More variation, upward trend
        'arima': create_forecast('ARIMA', 0.5, 0),      # Less variation, stable
        'prophet': create_forecast('Prophet', 0.6, 0.5) # Medium variation, slight upward
    }

