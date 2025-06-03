from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.database import client
import io
import matplotlib.pyplot as plt
import re

router = APIRouter()

def get_year_from_key(collection_name, key):
    if collection_name in [
        "emisja_zanieczyszczen_gazowych", "emisja_zanieczyszczen_pylowych",
        "grunty_wylaczone", "moc_instalowana", "scieki_przemyslowe", "zuzycie_energii"
    ]:
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

# 🔷 PNG - wykres liniowy
@router.get("/charts/{collection_name}.png")
async def get_chart_png(collection_name: str):
    collection = client["integracja"][collection_name]
    data = await collection.find().to_list(length=None)

    totals = {}
    for doc in data:
        for key, value in doc.items():
            year = get_year_from_key(collection_name, key)
            if year and value is not None and str(value).strip() != "":
                try:
                    amount = float(str(value).replace(",", "."))
                    totals[year] = totals.get(year, 0) + amount
                except Exception as e:
                    print(f"Błąd w polu {key}: {e}")

    if not totals:
        raise HTTPException(status_code=404, detail="Brak danych do wykresu")

    years = sorted(totals.keys())
    values = [totals[year] for year in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, values, marker='o', linestyle='-', color='blue')
    plt.xlabel("Rok")
    plt.ylabel("Wartość")
    plt.title(f"Wykres danych (liniowy): {collection_name}")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

# 🔷 JSON - dane interaktywne
@router.get("/charts/{collection_name}")
async def generate_chart(collection_name: str):
    collection = client["integracja"][collection_name]
    data = await collection.find().to_list(length=None)

    region_data = {}

    for doc in data:
        region_name = doc.get("Nazwa", "Nieznany")
        if region_name not in region_data:
            region_data[region_name] = []

        for key, value in doc.items():
            year = get_year_from_key(collection_name, key)
            if year and value is not None and str(value).strip() != "":
                try:
                    amount = float(str(value).replace(",", "."))
                    region_data[region_name].append({"year": year, "amount": amount})
                except Exception as e:
                    print(f"Błąd w polu {key}: {e}")

    # 🔥 Dodaj sprawdzenie pustych danych
    if not region_data:
        raise HTTPException(status_code=404, detail="Brak danych do interaktywnego wykresu")

    return [{"region": region, "data": sorted(entries, key=lambda x: x["year"])} for region, entries in region_data.items()]
