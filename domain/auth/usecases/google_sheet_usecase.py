import os
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from datetime import datetime
from authenticate_user import SCOPES

def get_sheets_google_drive(credentials: any) -> None:
    try:
        creds = Credentials.from_authorized_user_info(credentials, SCOPES)
        service = build("drive", "v3", credentials=creds)

        query = "mimeType = 'application/vnd.google-apps.spreadsheet'"
        # Call the Drive v3 API
        results = (
            service.files()
            .list(q=query, fields="nextPageToken, files(id, name)")
            .execute()
        )
        
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_google_sheet(credentials: any):
    try:
        output_dir = None
        access_token = credentials.get('token')
        file_name = "prueba-demo.xlsx"
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        export_url = f'https://www.googleapis.com/drive/v3/files/1McGqUNJ-O8XYkz494FBOG6cYpSItnM1tJn_k-IiB6v8/export?mimeType={mime_type}'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(export_url, headers=headers)
        
        if response.status_code == 200:
            if output_dir is None:
                output_dir = os.getcwd()
            
            os.makedirs(output_dir, exist_ok=True)
            
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Archivo descargado exitosamente: {file_path}")
            return file_path
        else:
            print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    
    except Exception as e:
        print(f"Error al descargar el archivo: {str(e)}")
        return None
    
    
def crear_google_sheet(credentials, titulo_hoja="Nueva Hoja de Cálculo"):
    """
    Crea una nueva hoja de cálculo de Google Sheets.
    
    Args:
        token: Token de acceso OAuth2
        titulo_hoja: Título para la nueva hoja de cálculo
    
    Returns:
        dict: Información sobre la hoja de cálculo creada, incluyendo su ID
    """
    try:
        # Crear credenciales a partir del token de acceso
        creds = Credentials.from_authorized_user_info(credentials, SCOPES)
        # Construir el servicio de Sheets
        service = build("drive", "v3", credentials=creds)
        
        # Definir propiedades de la hoja de cálculo
        file_metadata = {
            "name": titulo_hoja,
            "mimeType": "application/vnd.google-apps.spreadsheet"
        }   
        
        # Crear la solicitud para crear la hoja de cálculo
        file = service.files().create(body=file_metadata, fields="id").execute()
        
        print(f"Google Sheets creado con ID: {file.get('id')}")
        
        return {
            'titulo': titulo_hoja
        }
    
    except HttpError as error:
        print(f'Ocurrió un error: {error}')
        return {'error': str(error)}

def update_file_sheet(credentials: any):
    try:
        # create drive api client
        creds = Credentials.from_authorized_user_info(credentials, SCOPES)
        service = build("drive", "v3", credentials=creds)
        file_path = "prueba.xlsx"
        file_metadata = {"modifiedTime": datetime.utcnow().isoformat() + "Z"}
        media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # pylint: disable=maybe-no-member
        file_id = "1McGqUNJ-O8XYkz494FBOG6cYpSItnM1tJn_k-IiB6v8"
        file = (
            service.files().update(
                fileId=file_id, 
                body=file_metadata,
                media_body=media,
                fields="id, modifiedTime"
                )
            .execute()
        )
        print(f'Modified time: {file.get("modifiedTime")}')
        # delete_file()
    except Exception as e:
        print(f"Error al actualizar el archivo: {e}")
        
def delete_sheet(credentials: any):
    try:
        creds = Credentials.from_authorized_user_info(credentials, SCOPES)
        # Crear cliente de la API de Drive
        service = build("drive", "v3", credentials=creds)

        file_id = "1a8KyprQUpYRpUgPhP3I3e4Pza8pJES26UICtV4U35jM"  # Reemplaza con el ID real del archivo a eliminar

        # Eliminar el archivo
        service.files().delete(fileId=file_id).execute()

        print(f"Archivo con ID {file_id} eliminado correctamente.")

    except Exception as e:
        print(f"Error al eliminar el archivo: {e}")