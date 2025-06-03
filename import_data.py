"""
Plik import_data.py
---------------------
Skrypt do automatycznego importowania danych z plików JSON do MongoDB:
- Wczytuje pliki JSON z folderu ./json_files
- Wstawia dane do wybranych kolekcji w bazie danych
- Przydatny do wstępnego załadowania danych (seed) przy starcie aplikacji
"""

import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine  # (uwaga: w tym skrypcie nie jest wykorzystywany, ale zostawiamy w razie potrzeby)

# 🔹 MongoDB URI (pobrany np. z pliku database.py) — łączy się z MongoDB Atlas lub innym serwerem
MONGO_URI = "mongodb+srv://admin:admin@cluster0.7fugtco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "integracja"  # Nazwa bazy danych

# 🔹 Ścieżka do folderu, w którym znajdują się pliki JSON
JSON_FOLDER = "./json_files"  # Tutaj wrzuć swoje pliki JSON do importu

# 🔹 Lista plików JSON i docelowych kolekcji
FILES_TO_IMPORT = [
    ("Emisja zanieczyszczeń gazowych.json", "emisja_zanieczyszczen_gazowych"),
    ("Emisja zanieczyszczeń pyłowych.json", "emisja_zanieczyszczen_pylowych"),
    ("Ścieki przemysłowe odprowadzone w ciągu roku.json", "scieki_przemyslowe"),
    ("Grunty rolne i leśne wyłączone z produkcji rolniczej i leśnej.json", "grunty_wylaczone"),
    ("Zużycie energii elektrycznej przez SektorPrzemysłowy.json", "zuzycie_energii"),
    ("Moc zainstalowana i osiągalna w elektrowniach.json", "moc_instalowana"),
    ("Produkcja budowlano-montażowa.json", "produkcja_budowlana"),
    ("PRODUKCJA SPRZEDANA PRZEMYSŁU I BUDOWNICTWA.json", "produkcja_sprzedana")
]

# 🔹 Funkcja główna asynchroniczna
async def import_json_to_mongodb():
    # Inicjalizuje klienta MongoDB (asynchronicznego)
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]

    # 🔹 Pętla po wszystkich plikach do importu
    for filename, collection_name in FILES_TO_IMPORT:
        file_path = os.path.join(JSON_FOLDER, filename)

        # 🔹 Sprawdzenie, czy plik istnieje
        if not os.path.exists(file_path):
            print(f"❌ Plik {filename} nie został znaleziony. Pomijam.")
            continue

        # 🔹 Wczytanie danych z pliku JSON
        with open(file_path, encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Obsługa struktury, jeśli dane są w polu "TABLICA"
                if isinstance(data, dict) and "TABLICA" in data:
                    documents = data["TABLICA"]
                # Jeśli to lista — bierzemy całość
                elif isinstance(data, list):
                    documents = data
                # Jeśli to pojedynczy rekord — pakujemy w listę
                else:
                    documents = [data]
            except Exception as e:
                print(f"❌ Błąd podczas wczytywania {filename}: {e}")
                continue

        # 🔹 Czyścimy istniejącą kolekcję
        await db[collection_name].delete_many({})
        # 🔹 Wstawiamy dokumenty
        if documents:
            await db[collection_name].insert_many(documents)
            print(f"✅ Zaimportowano dane z {filename} do kolekcji '{collection_name}'.")
        else:
            print(f"⚠️ Plik {filename} jest pusty lub niepoprawny.")

    # 🔹 Zamykanie klienta po zakończeniu
    client.close()
    print("✅ Import zakończony.")

# 🔹 Uruchomienie funkcji asynchronicznej, jeśli skrypt jest uruchamiany bezpośrednio
if __name__ == "__main__":
    asyncio.run(import_json_to_mongodb())
