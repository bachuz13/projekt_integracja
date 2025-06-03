"""
Plik crud.py
-------------
Zawiera prostą funkcję do pobrania wszystkich rekordów z danej kolekcji MongoDB
przy użyciu ODMantic (AIOEngine).
"""

from odmantic import AIOEngine
from app.models import DynamicRecord

# Pobiera wszystkie rekordy z wybranej kolekcji
async def get_all_records(engine: AIOEngine, collection_name: str):
    collection = engine.motor_client["integracja"][collection_name]
    return await collection.find().to_list(length=None)
