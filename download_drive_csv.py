from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import os

# -------------------------------
# Google Drive API setup
# -------------------------------
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = service_account.Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)

# -------------------------------
# Google Drive folder ID
# -------------------------------
FOLDER_ID = '1gKU0QcOGv2chiDJ-Lp0xAPl1exnmegqo'

# -------------------------------
# Local download folder
# -------------------------------
DOWNLOAD_DIR = 'DATA'

# Create DATA folder if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -------------------------------
# List CSV files in Drive folder
# -------------------------------
results = service.files().list(
    q=f"'{FOLDER_ID}' in parents and mimeType='text/csv'",
    fields="files(id, name)"
).execute()

# -------------------------------
# Download each CSV into DATA/
# -------------------------------
for file in results.get('files', []):
    print(f"Downloading {file['name']}...")

    request = service.files().get_media(fileId=file['id'])

    file_path = os.path.join(DOWNLOAD_DIR, file['name'])

    with io.FileIO(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

    print(f"Saved to {file_path}")
