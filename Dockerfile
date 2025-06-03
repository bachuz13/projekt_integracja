FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y python3 python3-pip
# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj tylko zawartość folderu `app`, nie samego folderu
COPY app ./app
COPY frontend ./frontend
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
