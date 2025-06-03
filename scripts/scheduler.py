import asyncio
import httpx
from datetime import datetime
from app.database import engine
from app.models import AirEmission  # Możesz zmienić na inny model

EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/posts"

async def fetch_and_save_to_db():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(EXTERNAL_API_URL)
            response.raise_for_status()
            external_data = response.json()

            # Przykładowa transformacja danych do modelu AirEmission
            saved_count = 0
            for item in external_data[:5]:  # ograniczenie np. do 5 rekordów
                record = AirEmission(
                    name=item.get("title", "brak nazwy"),
                    value=len(item.get("body", "")) * 1.5,  # symulacja wartości
                    year=datetime.now().year
                )
                await engine.save(record)
                saved_count += 1

            print(f"[{datetime.now()}] Zapisano {saved_count} rekordów do bazy.")
    except Exception as e:
        print(f"[{datetime.now()}] Błąd pobierania/zapisu: {e}")

async def scheduler():
    while True:
        await fetch_and_save_to_db()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(scheduler())
