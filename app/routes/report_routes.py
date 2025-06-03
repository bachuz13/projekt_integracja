from fastapi import APIRouter, Query
from app.database import client
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

@router.get("/report/{collection_name}")
async def generate_report(collection_name: str, year: int = Query(...)):
    collection = client["integracja"][collection_name]
    data = await collection.find().to_list(length=None)

    regions = []

    for doc in data:
        region_name = doc.get("Nazwa", "Nieznany")
        region_total = 0

        for key, value in doc.items():
            found_year = get_year_from_key(collection_name, key)
            if found_year == year and value is not None and str(value).strip() != "":
                try:
                    value_str = str(value).replace(",", ".")
                    region_total += float(value_str)
                    print(f"Sumuję: {region_name}: {key} => {value} (rok={found_year})")
                except Exception as e:
                    print(f"Błąd przy przetwarzaniu {key}: {e}")

        regions.append({
            "region": region_name,
            "total": region_total
        })

    print(f"TOTALS: {regions}")
    return {
        "year": year,
        "regions": regions
    }
