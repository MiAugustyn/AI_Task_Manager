# run.py (identyczny dla obu serwisów)
from app import create_app

# Tworzymy instancję aplikacji
app = create_app()

if __name__ == '__main__':
    # Uruchamiamy serwer na porcie 5000, dostępny na wszystkich interfejsach
    app.run(debug=True, host='0.0.0.0', port=5000)