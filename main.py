import os
import json
import time
from fastapi.requests import Request
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from domain.auth.usecases.authenticate_user import get_auth_url, get_credentials_url
from domain.auth.usecases.google_sheet_usecase import get_sheets_google_drive, download_google_sheet, crear_google_sheet, delete_sheet,update_file_sheet
from domain.auth.usecases.edit_xlsx_usecase import update_row_sheet

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    if os.path.exists("token.json"):
        return RedirectResponse(url="/items")
    url = get_auth_url(request)
    return RedirectResponse(url=url)

@app.get("/callback", name="callback")
def get_credentials(request: Request):
    query_params = dict(request.query_params)
    get_credentials_url(query_params, request=request)
    return {"Credentials": "Created"}

@app.get("/items")
def read_item():
    with open("token.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    get_sheets_google_drive(credentials=credentials)
    return {"item_id":""}

@app.get("/sheet")
def download_sheet():
    start_time = time.time() * 1000
    with open("token.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    download_google_sheet(credentials=credentials)
    end_time = time.time() * 1000
    print(f"Time: {end_time - start_time}")
    return {"item_id":""}

@app.get("/update-row")
def update_row():
    update_row_sheet("hoja.xlsx", 0, "Columna1", "Nuevo Valor")
    
@app.get("/create-sheet")
def create_sheet():
    with open("token.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    crear_google_sheet(credentials=credentials)

@app.get("/delete")
def create_sheet():
    with open("token.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    delete_sheet(credentials=credentials)
    
@app.get("/update-sheet-google")
def create_sheet():
    start_time = time.time() * 1000
    with open("token.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    update_file_sheet(credentials=credentials)
    end_time = time.time() * 1000
    print(f"Time: {end_time - start_time}")
