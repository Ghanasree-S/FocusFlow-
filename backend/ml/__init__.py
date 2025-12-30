"""
FocusFlow ML Engine
Machine Learning models for productivity prediction and forecasting

Models:
- ProductivityClassifier: Random Forest for Low/Medium/High classification
- TimeSeriesForecaster: Ensemble of LSTM, ARIMA, and Prophet
- LSTMForecaster: Deep learning for complex pattern recognition
- ARIMAForecaster: Statistical forecasting for trends and seasonality
"""
from .data_processor import DataProcessor
from .productivity_classifier import ProductivityClassifier
from .time_series_forecaster import TimeSeriesForecaster
from .lstm_forecaster import LSTMForecaster
from .arima_forecaster import ARIMAForecaster

__all__ = [
    'DataProcessor',
    'ProductivityClassifier', 
    'TimeSeriesForecaster',
    'LSTMForecaster',
    'ARIMAForecaster'
]
