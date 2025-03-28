# Dockerfile – konfiguracja obrazu Dockera

# Używamy oficjalnego obrazu Pythona w wersji 3.9-slim
FROM python:3.9-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z wymaganiami do katalogu roboczego
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopiujemy resztę plików projektu do obrazu
COPY . .

# Udostępniamy port 5000
EXPOSE 5000

# Ustawiamy zmienną środowiskową wskazującą punkt startowy aplikacji Flask
ENV FLASK_APP=run.py

# Uruchamiamy aplikację przy użyciu Gunicorn z 4 workerami
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
