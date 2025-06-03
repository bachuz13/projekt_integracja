import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

# MongoDB URI z database.py
MONGO_URI = "mongodb+srv://admin:admin@cluster0.7fugtco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "integracja"

# Ścieżka do folderu z JSON-ami
JSON_FOLDER = "./json_files"  # <- Tutaj wrzuć swoje pliki JSON

# Lista plików i docelowych kolekcji
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

async def import_json_to_mongodb():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]

    for filename, collection_name in FILES_TO_IMPORT:
        file_path = os.path.join(JSON_FOLDER, filename)

        if not os.path.exists(file_path):
            print(f"❌ Plik {filename} nie został znaleziony. Pomijam.")
            continue

        with open(file_path, encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict) and "TABLICA" in data:
                    documents = data["TABLICA"]
                elif isinstance(data, list):
                    documents = data
                else:
                    documents = [data]
            except Exception as e:
                print(f"❌ Błąd podczas wczytywania {filename}: {e}")
                continue

        # Usuń istniejącą kolekcję (lub wyczyść)
        await db[collection_name].delete_many({})
        # Importuj dane
        if documents:
            await db[collection_name].insert_many(documents)
            print(f"✅ Zaimportowano dane z {filename} do kolekcji '{collection_name}'.")
        else:
            print(f"⚠️ Plik {filename} jest pusty lub niepoprawny.")

    client.close()
    print("✅ Import zakończony.")


if __name__ == "__main__":
    asyncio.run(import_json_to_mongodb())
