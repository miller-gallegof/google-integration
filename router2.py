import os
import json
from fastapi.requests import Request
from fastapi.responses import Response,JSONResponse
from google.oauth2.credentials import Credentials
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from domain.auth.usecases.authenticate_user import get_auth_url, get_sheets_google_drive, SCOPES, get_credentials_url, download_google_sheet
from domain.auth.usecases.edit_xlsx_usecase import update_row_sheet
from urllib.parse import urlencode
import httpx


# URL de Google OAuth 2.0
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

@app.get("/picker")
async def index():
    """Redirige a la autenticación de Google"""
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(auth_params)}"
    return RedirectResponse(auth_url)

@app.get("/picker/callback")
async def callback(request: Request):
    query_params = dict(request.query_params)
    """Recibe el código de autorización y obtiene el token"""
    if not query_params.get("code"):
        return JSONResponse(content={"error": "No authorization code provided"}, status_code=400)
    code = query_params.get("code")

    # Intercambiar código por token de acceso
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=token_data)
        token_info = response.json()
    
    if "access_token" not in token_info:
        return JSONResponse(content={"error": "Failed to obtain access token", "details": token_info}, status_code=400)

    return JSONResponse(content={"message": "Token obtained", "access_token": token_info["access_token"]})