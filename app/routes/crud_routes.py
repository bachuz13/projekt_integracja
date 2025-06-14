"""
Plik crud_routes.py
--------------------
Zawiera proste endpointy do pobierania danych z MongoDB
- pozwala na pobranie wszystkich dokumentów z danej kolekcji
"""

from fastapi import APIRouter, HTTPException
from app.database import engine, client
from app.models import DynamicRecord

router = APIRouter()

@router.get("/{collection_name}/")
async def get_data(collection_name: str):
    collection = client["integracja"][collection_name]
    data = await collection.find().to_list(length=None)
    return data
