import os

class Config:
    """Configuration settings for the Flask application."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    
    # API settings
    VULNERABILITY_SCANNER_API_URL = os.environ.get('VULNERABILITY_SCANNER_API_URL')
    VULNERABILITY_SCANNER_API_KEY = os.environ.get('VULNERABILITY_SCANNER_API_KEY')