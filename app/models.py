"""
Plik models.py
---------------
Definiuje model DynamicRecord używany przez ODMantic:
- Kod: kod regionu lub rekordu
- Nazwa: nazwa regionu lub rekordu
- extra_fields: dynamiczne pola (np. wartości dla lat)
"""

from odmantic import Model
from typing import Dict, Any

class DynamicRecord(Model):
    Kod: str
    Nazwa: str
    extra_fields: Dict[str, Any]
