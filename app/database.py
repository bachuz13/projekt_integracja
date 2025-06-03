"""
Plik database.py
-----------------
Ustawia połączenie z MongoDB Atlas
- definiuje klienta bazy danych (AsyncIOMotorClient)
- definiuje silnik ODMantic (AIOEngine)
"""

from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

# Zmienna do podstawienia własnego URI MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin@cluster0.7fugtco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(MONGO_URI)
engine = AIOEngine(client, database="integracja")
