# app/config.py
import os


class Config:
    # Ustawienia trybu debug oraz klucz sesji (pobrane z zmiennych środowiskowych lub domyślne)
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    SECRET_BUCKET = os.environ.get('AWS_S3_BUCKET')
    SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Konfiguracja bazy danych – używamy SQLite, ale można podmienić na np. RDS (DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
