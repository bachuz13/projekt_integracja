from pydantic import BaseModel
from typing import Dict, Any

class DynamicRecordOut(BaseModel):
    id: str
    Kod: str
    Nazwa: str
    extra_fields: Dict[str, Any]

    class Config:
        orm_mode = True
