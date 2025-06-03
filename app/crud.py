from odmantic import AIOEngine
from app.models import DynamicRecord

async def get_all_records(engine: AIOEngine, collection_name: str):
    collection = engine.motor_client["integracja"][collection_name]
    return await collection.find().to_list(length=None)
