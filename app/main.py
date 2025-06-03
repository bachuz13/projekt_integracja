from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os

from app.auth import authenticate_user, create_access_token
from app.routes import crud_routes, import_export_routes
from app.routes import report_routes, correlation_routes, chart_routes
from app import rest_api

app = FastAPI()

# --- Autoryzacja JWT ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Błędna nazwa użytkownika lub hasło")
    token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

# --- Routery aplikacji ---
app.include_router(crud_routes.router)
app.include_router(import_export_routes.router)
app.include_router(rest_api.router)
app.include_router(report_routes.router)
app.include_router(correlation_routes.router)
app.include_router(chart_routes.router)

# --- Pliki statyczne ---
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# --- Serwowanie strony głównej (panel) ---
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")

# --- Serwowanie strony logowania ---
@app.get("/login")
async def serve_login():
    return FileResponse("frontend/login.html")
