import io
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from authenticate_user import SCOPES

def get_folder_google_drive(credentials: any) -> None:
    creds = Credentials.from_authorized_user_info(credentials, SCOPES)
    service = build("drive", "v3", credentials=creds)
    results = (
            service.files()
            .update(fileId="", body="", fields="id, modifiedTime", media_body="")
            .execute()
        )
    items = results.get("files", [])
    return items

def upload_file_demo_first(credentials: any) -> None:
    creds = Credentials.from_authorized_user_info(credentials, SCOPES)
    service = build("drive", "v3", credentials=creds)
    file_id = "193XQkyM7-AF0Ot4BKhS3ry0hSQWUhkKaVuXxij8sm2M"
    
    file_name = "prueba-demo.xlsx"
    # export_mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # permissions = service.permissions().list(fileId=file_id, fields="permissions").execute()
    # print(permissions)
    try:
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None        
    
    if file is not None:
        with open(file_name, "wb") as f:
            f.write(file.getvalue())