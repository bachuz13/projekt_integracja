"""
Plik middleware.py
-------------------
Middleware FastAPI sprawdzający nagłówek JWT:
- przepuszcza wybrane ścieżki bez tokena (np. /login, /token, /static)
- weryfikuje token JWT w pozostałych endpointach
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.auth import SECRET_KEY, ALGORITHM

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Endpointy otwarte bez tokena
        open_paths = [
            "/login",
            "/token",
            "/static",
            "/docs", "/openapi.json", "/redoc"
        ]

        # Jeśli żądanie dotyczy otwartej ścieżki — przepuszczamy
        if any(request.url.path.startswith(path) for path in open_paths):
            return await call_next(request)

        # Sprawdzamy nagłówek Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token JWT wymagany")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Token JWT nieważny")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token JWT nieważny")

        return await call_next(request)
