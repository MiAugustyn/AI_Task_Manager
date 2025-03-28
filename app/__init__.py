# app/__init__.py
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
        # Importujemy blueprinty i rejestrujemy je w aplikacji:
        # - routes_bp: endpointy API (projekty, zadania)
        # - ai_bp: endpointy z logiką AI (np. przydzielanie zadania)
        # - analysis_bp: endpointy analizy (np. produktywności)
        # - views_bp: widoki strony WWW
        from .routes import routes_bp
        from .ai_routes import ai_bp
        from .analysis_routes import analysis_bp
        from .views import views_bp

        app.register_blueprint(routes_bp)
        app.register_blueprint(ai_bp, url_prefix='/ai')
        app.register_blueprint(analysis_bp, url_prefix='/analysis')
        app.register_blueprint(views_bp)  # Domyślny prefix (strona WWW)

        # Tworzymy tabele w bazie danych, jeśli jeszcze nie istnieją
        db.create_all()
        
    return app
