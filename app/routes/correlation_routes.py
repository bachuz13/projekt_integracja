"""
Plik correlation_routes.py
----------------------------
Endpoint obliczający współczynnik korelacji Pearsona między dwoma kolekcjami MongoDB
- Porównuje wartości dla wspólnych lat
- Obsługuje regiony
"""

from fastapi import APIRouter
from app.database import client
import numpy as np
import re

router = APIRouter()

def get_year_from_key(collection_name, key):
    if collection_name in ["emisja_zanieczyszczen_gazowych", "emisja_zanieczyszczen_pylowych",
                           "grunty_wylaczone", "moc_instalowana", "scieki_przemyslowe", "zuzycie_energii"]:
        match = re.search(r";(\d{4});", key)
        if match:
            return int(match.group(1))
    elif collection_name in ["produkcja_budowlana", "produkcja_sprzedana"]:
        matches = re.findall(r"(\d{4})", key)
        if matches:
            return int(matches[-1])
    else:
        matches = re.findall(r"(\d{4})", key)
        if matches:
            return int(matches[-1])
    return None

@router.get("/correlation/{collection1}/{collection2}")
async def calculate_correlation(collection1: str, collection2: str):
    col1 = client["integracja"][collection1]
    col2 = client["integracja"][collection2]

    data1 = await col1.find().to_list(length=None)
    data2 = await col2.find().to_list(length=None)

    values1 = {}
    values2 = {}

    for doc in data1:
        region_name = doc.get("Nazwa", "Nieznany")
        if region_name not in values1:
            values1[region_name] = {}
        for key, value in doc.items():
            year = get_year_from_key(collection1, key)
            if year and value is not None and str(value).strip() != "":
                try:
                    amount = float(str(value).replace(",", "."))
                    values1[region_name][year] = values1[region_name].get(year, 0) + amount
                except Exception as e:
                    print(f"Błąd w polu {key}: {e}")

    for doc in data2:
        region_name = doc.get("Nazwa", "Nieznany")
        if region_name not in values2:
            values2[region_name] = {}
        for key, value in doc.items():
            year = get_year_from_key(collection2, key)
            if year and value is not None and str(value).strip() != "":
                try:
                    amount = float(str(value).replace(",", "."))
                    values2[region_name][year] = values2[region_name].get(year, 0) + amount
                except Exception as e:
                    print(f"Błąd w polu {key}: {e}")

    results = []

    for region in values1:
        if region in values2:
            common_years = set(values1[region].keys()) & set(values2[region].keys())
            if len(common_years) >= 2:
                vals1 = [values1[region][y] for y in sorted(common_years)]
                vals2 = [values2[region][y] for y in sorted(common_years)]
                correlation = np.corrcoef(vals1, vals2)[0][1]
                results.append({
                    "region": region,
                    "common_years": sorted(common_years),
                    "correlation": round(float(correlation), 3)
                })

    return {"results": results}
