"""
FocusFlow Backend - Main Application Entry Point
Includes:
- Auto database seeding (creates demo user if not exists)
- Integrated activity tracker that runs in background
"""
import os
import sys
import threading
import time

# Force unbuffered output for real-time logging
sys.stdout.reconfigure(line_buffering=True)

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes import auth_bp, tasks_bp, activities_bp, focus_bp, insights_bp

# Activity Tracker Imports
import requests
try:
    import pygetwindow as gw
    TRACKER_AVAILABLE = True
except ImportError:
    TRACKER_AVAILABLE = False
    print("⚠️  pygetwindow not installed. Run: pip install pygetwindow", flush=True)

from datetime import datetime

# ============ ACTIVITY TRACKER ============

PRODUCTIVE_APPS = [
    'visual studio code', 'vscode', 'code', 'pycharm', 'intellij', 'webstorm',
    'sublime', 'atom', 'vim', 'nvim', 'terminal', 'cmd', 'powershell', 'git',
    'notion', 'obsidian', 'evernote', 'onenote', 'slack', 'teams', 'zoom',
    'figma', 'photoshop', 'illustrator', 'blender', 'unity', 'unreal',
    'excel', 'word', 'powerpoint', 'docs', 'sheets', 'slides',
    'postman', 'insomnia', 'mongodb', 'mysql', 'postgres', 'dbeaver'
]

DISTRACTING_APPS = [
    'youtube', 'netflix', 'prime video', 'disney', 'twitch', 'tiktok',
    'twitter', 'facebook', 'instagram', 'reddit', 'whatsapp', 'telegram',
    'discord', 'games', 'steam', 'epic games', 'spotify', 'vlc', 'media player'
]

def categorize_app(app_name: str) -> str:
    app_lower = app_name.lower()
    for prod_app in PRODUCTIVE_APPS:
        if prod_app in app_lower:
            return 'productive'
    for dist_app in DISTRACTING_APPS:
        if dist_app in app_lower:
            return 'distracting'
    return 'neutral'

def get_category_emoji(category: str) -> str:
    return {'productive': '🟢', 'distracting': '🔴', 'neutral': '🟡'}.get(category, '⚪')

def get_active_window():
    if not TRACKER_AVAILABLE:
        return None
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            title = active_window.title
            if ' - ' in title:
                parts = title.split(' - ')
                app_name = parts[-1].strip()
            else:
                app_name = title
            return {'title': title, 'app_name': app_name}
    except:
        pass
    return None

def tracker_login(email: str, password: str) -> str:
    try:
        response = requests.post('http://localhost:5000/api/auth/login', json={
            'email': email, 'password': password
        }, timeout=5)
        if response.status_code == 200:
            return response.json().get('token')
    except Exception as e:
        print(f"[TRACKER] Login error: {e}", flush=True)
    return None

def log_activity(token: str, app_name: str, duration_minutes: float, category: str):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            'http://localhost:5000/api/activities',
            json={
                'app_name': app_name,
                'duration_minutes': duration_minutes,
                'category': category,
                'timestamp': datetime.utcnow().isoformat()
            },
            headers=headers, timeout=5
        )
        return response.status_code == 201
    except Exception as e:
        print(f"[TRACKER] API error: {e}", flush=True)
    return False

def run_tracker_thread(email: str, password: str, interval: int = 10):
    """Background tracker thread - logs every 10 seconds"""
    print("", flush=True)
    print("🎯 ACTIVITY TRACKER: Waiting for server...", flush=True)
    time.sleep(3)
    
    token = None
    retry_count = 0
    
    while not token and retry_count < 5:
        token = tracker_login(email, password)
        if not token:
            retry_count += 1
            print(f"🎯 ACTIVITY TRACKER: Login attempt {retry_count}/5...", flush=True)
            time.sleep(2)
    
    if not token:
        print("🎯 ACTIVITY TRACKER: ❌ Login failed!", flush=True)
        return
    
    print("🎯 ACTIVITY TRACKER: ✅ Login successful!", flush=True)
    print(f"🎯 ACTIVITY TRACKER: 📊 Tracking every {interval} seconds", flush=True)
    print("=" * 70, flush=True)
    print("TIME      | CURRENT WINDOW                              | STATUS", flush=True)
    print("=" * 70, flush=True)
    
    current_app = None
    app_start_time = time.time()
    records_saved = 0
    
    while True:
        try:
            window_info = get_active_window()
            ts = datetime.now().strftime('%H:%M:%S')
            
            if window_info:
                app_name = window_info['app_name'][:40]
                category = categorize_app(app_name)
                emoji = get_category_emoji(category)
                
                print(f"[{ts}] | {app_name:<43} | {emoji} Tracking", flush=True)
                
                if current_app and current_app != window_info['app_name']:
                    duration = (time.time() - app_start_time) / 60
                    prev_category = categorize_app(current_app)
                    
                    if duration >= 0.05:
                        success = log_activity(token, current_app, round(duration, 2), prev_category)
                        if success:
                            records_saved += 1
                            prev_emoji = get_category_emoji(prev_category)
                            print(f"[{ts}] | 💾 SAVED TO DB: {current_app[:30]} | {prev_emoji} {duration:.2f}min (#{records_saved})", flush=True)
                    
                    app_start_time = time.time()
                
                current_app = window_info['app_name']
            else:
                print(f"[{ts}] | (No active window)                          | ⚪ Waiting", flush=True)
            
            time.sleep(interval)
        except Exception as e:
            print(f"[{ts}] | ERROR: {str(e)[:35]}                  | ⚠️", flush=True)
            time.sleep(interval)

def test_mongodb_and_seed():
    """Test MongoDB connection and create demo user if needed"""
    print("", flush=True)
    print("📊 Connecting to MongoDB...", flush=True)
    
    try:
        from utils.db import get_db
        from models.user import UserModel
        
        db = get_db()
        collections = db.list_collection_names()
        
        print(f"✅ MongoDB Connected!", flush=True)
        print(f"   Database: {Config.MONGO_DB_NAME}", flush=True)
        print(f"   Collections: {', '.join(collections) if collections else '(new database)'}", flush=True)
        
        # Auto-create demo user if not exists
        print("", flush=True)
        print("👤 Checking demo user...", flush=True)
        
        user_model = UserModel(db)
        existing_user = user_model.find_by_email('demo@focusflow.ai')
        
        if existing_user:
            print("   ✅ Demo user exists", flush=True)
        else:
            user_model.create_user(
                name='Demo User',
                email='demo@focusflow.ai',
                password='demo123',
                style='Balanced',
                goals=['Improve focus', 'Track productivity']
            )
            print("   ✅ Demo user created!", flush=True)
        
        print("   Email: demo@focusflow.ai", flush=True)
        print("   Password: demo123", flush=True)
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Connection Failed!", flush=True)
        print(f"   Error: {str(e)}", flush=True)
        print("", flush=True)
        print("   Please check:", flush=True)
        print("   1. .env file has correct MONGO_URI", flush=True)
        print("   2. MongoDB Atlas IP whitelist includes your IP", flush=True)
        return False

# ============ FLASK APP ============

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(focus_bp)
    app.register_blueprint(insights_bp)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'FocusFlow API', 'version': '1.0.0'})
    
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({'message': 'Welcome to FocusFlow API'})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    print("", flush=True)
    print("=" * 70, flush=True)
    print("🚀 FOCUSFLOW BACKEND SERVER", flush=True)
    print("=" * 70, flush=True)
    
    # Test MongoDB and auto-seed
    if not test_mongodb_and_seed():
        print("", flush=True)
        print("⚠️  Cannot start without MongoDB. Exiting.", flush=True)
        sys.exit(1)
    
    print("", flush=True)
    print("🌐 Server: http://localhost:5000", flush=True)
    print("", flush=True)
    print("📡 API Endpoints:", flush=True)
    print("   POST /api/auth/login", flush=True)
    print("   GET  /api/insights/dashboard", flush=True)
    print("   GET  /api/insights/forecast", flush=True)
    print("=" * 70, flush=True)
    
    # Start tracker
    if TRACKER_AVAILABLE:
        tracker_thread = threading.Thread(
            target=run_tracker_thread,
            args=('demo@focusflow.ai', 'demo123', 60),
            daemon=True
        )
        tracker_thread.start()
    else:
        print("⚠️  Install pygetwindow: pip install pygetwindow", flush=True)
    
    print("", flush=True)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
