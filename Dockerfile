# Plik Dockerfile
# -----------------
# Konfiguracja obrazu Docker do uruchomienia aplikacji FastAPI.
# - Używa obrazu bazowego python:3.12-slim
# - Kopiuje aplikację i frontend
# - Instalacja zależności
# - Uruchamia aplikację z uvicorn

# 🔹 Używamy oficjalnego, lekkiego obrazu Pythona (Python 3.12 w wersji slim)
FROM python:3.12-slim

# 🔹 Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# 🔹 Kopiujemy tylko zawartość folderu `app` (np. pliki .py) do katalogu /app/app
# - Nie kopiujemy całego folderu `app` jako folderu, tylko jego zawartość
COPY app ./app

# 🔹 Kopiujemy zawartość folderu frontend (np. pliki HTML/JS/CSS) do katalogu /app/frontend
COPY frontend ./frontend

# 🔹 Kopiujemy plik requirements.txt (z listą zależności Pythona) do katalogu roboczego
COPY requirements.txt .

# 🔹 Instalujemy zależności z pliku requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Domyślne polecenie uruchamiające aplikację FastAPI za pomocą uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
