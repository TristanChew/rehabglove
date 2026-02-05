from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = service_account.Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

FOLDER_ID = '1gKU0QcOGv2chiDJ-Lp0xAPl1exnmegqo'

results = service.files().list(
    q=f"'{FOLDER_ID}' in parents and mimeType='text/csv'",
    fields="files(id, name)"
).execute()

for file in results['files']:
    request = service.files().get_media(fileId=file['id'])
    fh = io.FileIO(file['name'], 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
