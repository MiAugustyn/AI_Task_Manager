# task_assign_service/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicjalizacja obiektu SQLAlchemy, który będzie obsługiwał bazę danych
db = SQLAlchemy()

def create_app():
    # Tworzymy instancję aplikacji Flask
    app = Flask(__name__)
    # Ładujemy konfigurację z pliku config.py
    app.config.from_object('app.config.Config')

    # Inicjalizujemy SQLAlchemy z aplikacją
    db.init_app(app)

    with app.app_context():
        # Importujemy blueprint dla zadań AI
        from .ai_routes import ai_bp

        # Rejestrujemy blueprint - tutaj bez prefiksu, bo to główny endpoint tego serwisu
        app.register_blueprint(ai_bp)

        # Tworzymy tabele w bazie danych, jeśli jeszcze nie istnieją
        db.create_all()
        
    return app