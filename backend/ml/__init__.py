"""
ChronosAI ML Engine
Machine Learning models for productivity prediction and forecasting

Core Models:
- ProductivityClassifier: Random Forest for Low/Medium/High classification
- TimeSeriesForecaster: Ensemble of LSTM, ARIMA, and Prophet
- LSTMForecaster: Deep learning for complex pattern recognition
- ARIMAForecaster: Statistical forecasting for trends and seasonality

Novel Research Models:
- SHAPExplainer: SHAP-based explainable AI for productivity classification
- DigitalFatigueIndex: Real-time cognitive fatigue scoring from behavioral signals
- ContextSwitchAnalyzer: Context-switch cost & attention residue modeling
- ProcrastinationDetector: Sequential pattern mining for procrastination triggers
- AdaptiveEnsembleOptimizer: Dynamic per-user ensemble weight adaptation
- MoodProductivityVAR: Bidirectional mood ↔ productivity VAR / Granger causality
"""
from .data_processor import DataProcessor
from .productivity_classifier import ProductivityClassifier
from .time_series_forecaster import TimeSeriesForecaster
from .lstm_forecaster import LSTMForecaster
from .arima_forecaster import ARIMAForecaster
from .shap_explainer import SHAPExplainer
from .fatigue_index import DigitalFatigueIndex
from .context_switch import ContextSwitchAnalyzer
from .procrastination_detector import ProcrastinationDetector
from .adaptive_ensemble import AdaptiveEnsembleOptimizer
from .mood_productivity_var import MoodProductivityVAR

__all__ = [
    'DataProcessor',
    'ProductivityClassifier', 
    'TimeSeriesForecaster',
    'LSTMForecaster',
    'ARIMAForecaster',
    'SHAPExplainer',
    'DigitalFatigueIndex',
    'ContextSwitchAnalyzer',
    'ProcrastinationDetector',
    'AdaptiveEnsembleOptimizer',
    'MoodProductivityVAR',
]
