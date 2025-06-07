import os
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Google Drive API scopes ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# --- Replace this with your actual Google Drive folder ID ---
# To find the folder ID:
# 1. Go to Google Drive in browser
# 2. Open the folder where you want to upload
# 3. The URL looks like https://drive.google.com/drive/folders/<FOLDER_ID>
folder_id = '1Sr7ODdt4jFCXQJ6O6u42ORbZDndtPDmB'

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def upload_media():
    service = authenticate()
    media_folder = 'media'

    for filename in os.listdir(media_folder):
        filepath = os.path.join(media_folder, filename)
        if os.path.isfile(filepath):
            print(f"Uploading {filename} to Google Drive folder ID {folder_id}...")
            file_metadata = {
                'name': filename,
                'parents': [folder_id]  # upload to specific folder
            }
            media = MediaFileUpload(filepath, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def sync_code():
    try:
        subprocess.run(["git", "add", "code/"], check=True)
        subprocess.run(["git", "commit", "-m", "Sync code changes"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Code synced to GitHub.")
    except subprocess.CalledProcessError:
        print("No new code changes to push or already committed.")

if __name__ == "__main__":
    upload_media()
