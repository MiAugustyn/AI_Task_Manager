# app/config.py
import os

class Config:
    # Ustawienia trybu debug oraz klucz sesji (pobrane z zmiennych środowiskowych lub domyślne)
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    # Konfiguracja bazy danych – używamy SQLite, ale można podmienić na np. RDS (DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
