# app/config.py
import os


class Config:
    # Ustawienia trybu debug oraz klucz sesji (pobrane z zmiennych środowiskowych lub domyślne)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Konfiguracja bazy danych – używamy SQLite, ale można podmienić na np. RDS (DATABASE_URL)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Haslo123!@database-1.cha0w2kkszs3.eu-north-1.rds.amazonaws.com:3306/taskmanagerdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
