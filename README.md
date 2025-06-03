# 📊 Projekt Integracji Danych: Rozwój Przemysłu i Stan Środowiska

## 📌 Opis projektu
Projekt ma na celu integrację i analizę danych dotyczących rozwoju przemysłu oraz stanu środowiska w Polsce, pozyskanych z portalu [BDL (Bank Danych Lokalnych)](https://bdl.stat.gov.pl/bdl/dane/podgrup/temat). Dane te są analizowane w celu wykrycia zależności, generowania raportów i wizualizacji, a także umożliwienia użytkownikom ich przeglądania za pomocą REST API oraz interfejsu webowego.

---

## 📁 Struktura katalogów

```bash
.
├── app/
│ ├── auth.py
│ ├── crud.py
│ ├── database.py
│ ├── main.py
│ ├── middleware.py
│ ├── models.py
│ ├── rest_api.py
│ ├── schemas.py
│ └── routes/
│ ├── chart_routes.py
│ ├── correlation_routes.py
│ ├── crud_routes.py
│ ├── import_export_routes.py
│ └── report_routes.py
│
├── frontend/
│ ├── app.js
│ ├── index.html
│ ├── login.html
│ ├── login.js
│ ├── login.css
│ └── styles.css
│
├── json_files/
│ ├── Emisja zanieczyszczeń gazowych.json
│ ├── Emisja zanieczyszczeń pyłowych.json
│ ├── Grunty rolne i leśne wyłączone z produkcji rolniczej.json
│ ├── Moc zainstalowana i osiągalna w elektrowniach.json
│ ├── Produkcja budowlano-montażowa.json
│ ├── Produkcja sprzedana przemysłu i budownictwa.json
│ ├── Zużycie energii elektrycznej przez sektor przemysłowy.json
│ └── Ścieki przemysłowe odprowadzone w ciągu roku.json
│
├── import_data.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── run_project.ps1
└── README.md
```

---

## 📦 Opis głównych plików i katalogów

### Backend (`app/`)
- **auth.py** — logika uwierzytelniania użytkowników.
- **crud.py** — obsługa operacji CRUD na danych przemysłowych i środowiskowych.
- **database.py** — konfiguracja połączenia z bazą danych (SQLAlchemy).
- **main.py** — uruchamianie aplikacji FastAPI.
- **middleware.py** — obsługa CORS i innych middleware’ów.
- **models.py** — definicje modeli ORM.
- **rest_api.py** — definicja głównych endpointów API.
- **schemas.py** — walidacja danych i struktury odpowiedzi API (Pydantic).
- **routes/** — osobne moduły dla:
  - `chart_routes.py` — generowanie wykresów na podstawie danych.
  - `correlation_routes.py` — obliczanie korelacji pomiędzy wskaźnikami przemysłu i środowiska.
  - `crud_routes.py` — podstawowe operacje CRUD.
  - `import_export_routes.py` — importowanie danych z JSON/CSV oraz eksport.
  - `report_routes.py` — generowanie raportów.

### Frontend (`frontend/`)
- **index.html** — strona główna aplikacji (panel użytkownika).
- **login.html / login.js / login.css** — ekran logowania i obsługa uwierzytelniania.
- **app.js** — logika aplikacji frontendowej.
- **styles.css** — ogólne style CSS.

### Dane (`json_files/`)
Pliki JSON pobrane z portalu BDL (emisje, produkcja przemysłu, zużycie energii itp.).

---

## 📈 Funkcjonalności projektu

✅ Importowanie danych z plików JSON przy użyciu `import_data.py` lub endpointu API.  
✅ REST API do:
- logowania i uwierzytelniania (token JWT),
- generowania wykresów (np. słupkowe, liniowe),
- obliczania współczynników korelacji (np. Pearsona) pomiędzy wskaźnikami przemysłu i środowiska,
- operacji CRUD na danych,
- importowania/eksportowania danych w formatach JSON/CSV,
- generowania raportów analitycznych (JSON lub CSV).

✅ Analiza danych:
- agregacja danych według województw, lat lub wskaźników,
- normalizacja wskaźników w celu porównań regionalnych,
- obsługa brakujących danych.

✅ Wizualizacje danych:
- tworzenie wykresów trendów i wykresów porównawczych,
- eksport wykresów do PNG.

✅ Frontend:
- ekran logowania z uwierzytelnianiem JWT,
- dashboard do wyświetlania danych i raportów.

✅ Obsługa uwierzytelniania JWT.

✅ Obsługa Dockera:
- plik `Dockerfile` do budowania obrazu aplikacji,
- plik `docker-compose.yml` do uruchamiania w kontenerach.

---

## 🔧 Instalacja

**Klonowanie repozytorium**
```bash
git clone https://github.com/twoj-login/integration_project.git
cd integration_project
Utworzenie środowiska wirtualnego
```
```bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Instalacja zależności

```bash
pip install -r requirements.txt
```
🚀 Uruchamianie projektu
Opcja 1: Uruchamianie za pomocą skryptu PowerShell
```bash
.\run_project.ps1
```
Skrypt uruchamia backend, frontend oraz w razie potrzeby wykonuje dodatkowe kroki (np. import danych lub migracje bazy danych).

Opcja 2: Uruchamianie za pomocą Docker Compose
```bash
docker-compose up --build
```
Uruchamia aplikację w kontenerach, umożliwiając szybkie wdrożenie na dowolnym środowisku.

📂 Import danych
Do importu danych z folderu json_files/ służy skrypt:

```bash
python import_data.py
```
Alternatywnie można wykorzystać endpoint /import w API.

🧩 Zależności
Python 3.8+

FastAPI

SQLAlchemy

Pandas

Matplotlib

Uvicorn

Wszystkie zależności zostały zdefiniowane w pliku requirements.txt.
