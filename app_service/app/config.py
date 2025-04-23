
# app_service/app/config.py
import os

class Config:
    # Ustawienia trybu debug oraz klucz sesji (pobrane z zmiennych środowiskowych lub domyślne)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    
    # Konfiguracja bazy danych
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False