import io
import os
import requests
from fastapi.requests import Request
from fastapi.responses import Response
from typing import List, Optional
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"
          ]

def get_auth_url(request: Request) -> Optional[str]:
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file="cliente_secret_last.json",
            scopes=SCOPES
        )
        flow.redirect_uri = request.url_for('callback')
        auth_url, _ = flow.authorization_url(prompt="consent", access_type='offline')
        return auth_url
    except Exception as e:
        return e

def get_credentials_url(params: dict, request: Request) -> Optional[str]:
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file="cliente_secret_last.json",
            scopes=SCOPES,
            state=params.get("state", None)
        )
        flow.redirect_uri = request.url_for('callback')
        flow.fetch_token(code=params.get("code"))
        credentials = flow.credentials
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
        return credentials
    except Exception as e:
        return e
        
        
def get_credentials_by_server()-> Optional[str]:
    flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file="cliente_secret_last.json",
            scopes=SCOPES
        )
    flow.redirect_uri = "http://localhost:8000/callback"
    creds = flow.run_local_server(port=8000)
    return creds
        
def delete_file():
    file_path = "prueba.xlsx"

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Archivo eliminado: {file_path}")
    else:
        print("El archivo no existe")