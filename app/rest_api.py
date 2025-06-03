from fastapi import APIRouter, HTTPException, Query
from app.database import client
import re

router = APIRouter()

@router.get("/external/fetch")
async def fetch_data_from_mongo(
    collection: str = Query(..., description="Nazwa kolekcji"),
    limit: int = Query(10, description="Limit wyników"),
    page: int = Query(1, description="Numer strony"),
    year: int = Query(None, description="Rok (opcjonalnie)"),
    region: str = Query(None, description="Region (opcjonalnie)"),
    sort: str = Query("asc", description="Sortowanie: 'asc' lub 'desc'")
):
    """
    Endpoint do pobierania danych z MongoDB z filtrami: kolekcja, rok, region, paginacja, sortowanie.
    """
    try:
        db = client["integracja"]
        if collection not in await db.list_collection_names():
            raise HTTPException(status_code=404, detail=f"Kolekcja '{collection}' nie istnieje w bazie danych.")

        query = {}
        if region:
            query["Nazwa"] = region.upper()

        sort_direction = 1 if sort == "asc" else -1

        cursor = db[collection].find(query).sort("_id", sort_direction)
        raw_data = await cursor.to_list(length=None)  # Pobieramy wszystko (bo filtr roku i dynamiczne pola muszą być w Pythonie)

        filtered_data = []
        for doc in raw_data:
            doc.pop("_id", None)
            if year:
                year_keys = [key for key in doc.keys() if str(year) in key]
                if not year_keys:
                    continue
                values = [float(str(doc[k]).replace(",", ".")) for k in year_keys if doc[k] is not None and str(doc[k]).strip() != ""]
                if not values:
                    continue
                doc = {"Nazwa": doc.get("Nazwa", "Nieznany"), "rok": year, "suma": sum(values)}
            filtered_data.append(doc)

        total_count = len(filtered_data)

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_data = filtered_data[start_idx:end_idx]

        return {
            "source": f"MongoDB kolekcja: {collection}",
            "count": total_count,
            "page": page,
            "limit": limit,
            "sort": sort,
            "sample": paginated_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania danych: {str(e)}")

