import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')
    DEBUG = os.environ.get('DEBUG', 'false').lower() in ('1', 'true', 'yes', 'on')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'