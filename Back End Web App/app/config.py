import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///house_pricing.db')
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/house_pricing_model.pkl')