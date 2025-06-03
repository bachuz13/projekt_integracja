from odmantic import Model
from typing import Dict, Any

class DynamicRecord(Model):
    Kod: str
    Nazwa: str
    extra_fields: Dict[str, Any]
