"""
Time Series Forecasting Model
Uses Prophet/ARIMA-style patterns for productivity forecasting
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pickle
import os
from .data_processor import DataProcessor

class TimeSeriesForecaster:
    """
    Time series forecaster for productivity predictions
    
    Predicts:
    - Next 7 days focus time
    - Workload trends
    - Task completion probability
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.data_processor = DataProcessor()
        self.model_path = model_path or os.path.join(os.path.dirname(__file__), 'models', 'forecaster.pkl')
        
        # Try to load existing model
        self._load_model()
    
    def _load_model(self):
        """Load trained model from disk if available"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
        except Exception as e:
            print(f"Could not load forecaster model: {e}")
            self.model = None
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
        except Exception as e:
            print(f"Could not save forecaster model: {e}")
    
    def train(self, historical_data: pd.DataFrame):
        """
        Train the forecasting model
        
        Args:
            historical_data: DataFrame with columns 'ds' (datetime) and 'y' (value)
        """
        try:
            from prophet import Prophet
            
            self.model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False,
                changepoint_prior_scale=0.05
            )
            
            self.model.fit(historical_data[['ds', 'y']])
            self._save_model()
            
        except ImportError:
            print("Prophet not available, using statistical fallback")
            self.model = self._create_statistical_model(historical_data)
    
    def _create_statistical_model(self, data: pd.DataFrame) -> dict:
        """Create simple statistical model as fallback"""
        if data.empty:
            return {
                'mean': 60,
                'std': 20,
                'trend': 0,
                'weekly_pattern': [1.0] * 7
            }
        
        # Calculate basic statistics
        mean_val = data['y'].mean()
        std_val = data['y'].std()
        
        # Calculate trend (slope)
        if len(data) > 1:
            x = np.arange(len(data))
            coeffs = np.polyfit(x, data['y'].values, 1)
            trend = coeffs[0]
        else:
            trend = 0
        
        # Weekly pattern (if enough data)
        weekly_pattern = [1.0] * 7
        if len(data) >= 7:
            data['dayofweek'] = data['ds'].dt.dayofweek
            weekly_means = data.groupby('dayofweek')['y'].mean()
            overall_mean = data['y'].mean()
            weekly_pattern = [
                weekly_means.get(i, overall_mean) / overall_mean if overall_mean > 0 else 1.0
                for i in range(7)
            ]
        
        return {
            'mean': mean_val if not np.isnan(mean_val) else 60,
            'std': std_val if not np.isnan(std_val) else 20,
            'trend': trend if not np.isnan(trend) else 0,
            'weekly_pattern': weekly_pattern
        }
    
    def forecast(self, weekly_trends: list, periods: int = 7) -> dict:
        """
        Forecast productivity for future days
        
        Args:
            weekly_trends: Historical daily activity data
            periods: Number of days to forecast
            
        Returns:
            Dict with forecast data
        """
        # Prepare data
        df = self.data_processor.prepare_timeseries_data(weekly_trends)
        
        # If no model or data, return rule-based forecast
        if df.empty or len(df) < 3:
            return self._generate_fallback_forecast(weekly_trends, periods)
        
        try:
            # Try Prophet forecasting
            if self.model is not None and hasattr(self.model, 'predict'):
                future = self.model.make_future_dataframe(periods=periods)
                forecast = self.model.predict(future)
                
                return self._format_prophet_forecast(forecast, weekly_trends, periods)
            else:
                # Use statistical forecasting
                return self._statistical_forecast(df, weekly_trends, periods)
                
        except Exception as e:
            print(f"Forecasting failed: {e}")
            return self._generate_fallback_forecast(weekly_trends, periods)
    
    def _statistical_forecast(self, df: pd.DataFrame, weekly_trends: list, periods: int) -> dict:
        """Generate forecast using statistical methods"""
        stats = self._create_statistical_model(df)
        
        # Generate forecast
        weekly_forecast = []
        base_date = datetime.utcnow()
        
        for i in range(periods):
            future_date = base_date + timedelta(days=i + 1)
            day_of_week = future_date.weekday()
            
            # Calculate predicted value
            base_value = stats['mean'] + stats['trend'] * (len(df) + i)
            seasonal_factor = stats['weekly_pattern'][day_of_week]
            predicted = max(0, base_value * seasonal_factor)
            
            weekly_forecast.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'day': future_date.strftime('%A'),
                'predicted_productive_minutes': round(predicted),
                'confidence': 0.7 - (i * 0.05)  # Confidence decreases over time
            })
        
        # Calculate summary metrics
        avg_predicted = np.mean([f['predicted_productive_minutes'] for f in weekly_forecast])
        current_avg = df['y'].mean() if not df.empty else 60
        
        # Determine trend
        if avg_predicted > current_avg * 1.1:
            trend = 'Up'
        elif avg_predicted < current_avg * 0.9:
            trend = 'Down'
        else:
            trend = 'Stable'
        
        return {
            'next_day_workload': min(100, round(weekly_forecast[0]['predicted_productive_minutes'] / 3)),
            'completion_probability': min(95, max(50, round(70 + (avg_predicted - 60) / 5))),
            'best_focus_window': self.data_processor.detect_best_focus_hours([]),
            'distraction_trigger': self.data_processor.detect_distraction_triggers([]),
            'trend': trend,
            'weekly_forecast': weekly_forecast,
            'load_level': self._categorize_workload(avg_predicted),
            'stress_risk': self._calculate_stress_risk(weekly_trends)
        }
    
    def _format_prophet_forecast(self, forecast: pd.DataFrame, weekly_trends: list, periods: int) -> dict:
        """Format Prophet forecast output"""
        recent_forecast = forecast.tail(periods)
        
        weekly_forecast = []
        for _, row in recent_forecast.iterrows():
            weekly_forecast.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'day': row['ds'].strftime('%A'),
                'predicted_productive_minutes': round(max(0, row['yhat'])),
                'lower_bound': round(max(0, row['yhat_lower'])),
                'upper_bound': round(row['yhat_upper']),
                'confidence': 0.8
            })
        
        avg_predicted = np.mean([f['predicted_productive_minutes'] for f in weekly_forecast])
        
        return {
            'next_day_workload': min(100, round(weekly_forecast[0]['predicted_productive_minutes'] / 3)),
            'completion_probability': min(95, max(50, round(70 + (avg_predicted - 60) / 5))),
            'best_focus_window': self.data_processor.detect_best_focus_hours([]),
            'distraction_trigger': self.data_processor.detect_distraction_triggers([]),
            'trend': self._determine_trend(weekly_forecast),
            'weekly_forecast': weekly_forecast,
            'load_level': self._categorize_workload(avg_predicted),
            'stress_risk': self._calculate_stress_risk(weekly_trends)
        }
    
    def _generate_fallback_forecast(self, weekly_trends: list, periods: int) -> dict:
        """Generate fallback forecast when data is insufficient"""
        # Calculate base from available data or use defaults
        if weekly_trends:
            avg_productive = np.mean([t.get('productive_minutes', 60) for t in weekly_trends])
        else:
            avg_productive = 60
        
        weekly_forecast = []
        base_date = datetime.utcnow()
        
        # Day-of-week modifiers (typical work pattern)
        day_modifiers = [1.0, 1.1, 1.1, 1.0, 0.95, 0.7, 0.6]  # Mon-Sun
        
        for i in range(periods):
            future_date = base_date + timedelta(days=i + 1)
            day_of_week = future_date.weekday()
            
            predicted = avg_productive * day_modifiers[day_of_week]
            predicted += np.random.normal(0, 10)  # Add some variance
            
            weekly_forecast.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'day': future_date.strftime('%A'),
                'predicted_productive_minutes': round(max(0, predicted)),
                'confidence': 0.6
            })
        
        return {
            'next_day_workload': 75,
            'completion_probability': 82,
            'best_focus_window': '09:00 AM - 11:30 AM',
            'distraction_trigger': 'Social Media / Morning Emails',
            'trend': 'Stable',
            'weekly_forecast': weekly_forecast,
            'load_level': 'Medium',
            'stress_risk': 'Low'
        }
    
    def _determine_trend(self, weekly_forecast: list) -> str:
        """Determine overall trend from forecast"""
        if len(weekly_forecast) < 2:
            return 'Stable'
        
        values = [f['predicted_productive_minutes'] for f in weekly_forecast]
        first_half_avg = np.mean(values[:len(values)//2])
        second_half_avg = np.mean(values[len(values)//2:])
        
        if second_half_avg > first_half_avg * 1.1:
            return 'Up'
        elif second_half_avg < first_half_avg * 0.9:
            return 'Down'
        return 'Stable'
    
    def _categorize_workload(self, avg_minutes: float) -> str:
        """Categorize workload level"""
        if avg_minutes < 60:
            return 'Light'
        elif avg_minutes < 180:
            return 'Medium'
        else:
            return 'Heavy'
    
    def _calculate_stress_risk(self, weekly_trends: list) -> str:
        """Calculate stress risk based on patterns"""
        if not weekly_trends:
            return 'Low'
        
        # High distraction combined with high workload = stress
        total_distraction = sum(t.get('distracting_minutes', 0) for t in weekly_trends)
        total_productive = sum(t.get('productive_minutes', 0) for t in weekly_trends)
        
        distraction_ratio = total_distraction / max(total_distraction + total_productive, 1)
        
        if distraction_ratio > 0.4:
            return 'High'
        elif distraction_ratio > 0.25:
            return 'Medium'
        return 'Low'
