from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def delete_file(file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        print(f'File ID: {file_id} deleted successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def search_file_by_name(file_name, folder_id):
    print(f"Searching for file: {file_name} in folder ID: {folder_id}")
    query = f"name = '{file_name}' and '{folder_id}' in parents"
    results = service.files().list(
        q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No file found.')
        return None
    else:
        print(f"Found file: Name: {items[0]['name']}, ID: {items[0]['id']}")
        return items[0]['id']

def first_delete(file_name, folder_id):
    # Search for an existing file with the same name
    existing_file_id = search_file_by_name(file_name, folder_id)
    if existing_file_id:
        # Delete the existing file
        delete_file(existing_file_id)
   
def upload_file(file_name, file_path, folder_id):
    # Search for an existing file with the same name
    existing_file_id = search_file_by_name(file_name, folder_id)
    if existing_file_id:
        # Delete the existing file
        delete_file(existing_file_id)
   
    print(f"Uploading file: {file_path} to folder ID: {folder_id}")
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')
    return file.get('id')

def download_file(file_id, file_path):
    print(f"Downloading file ID: {file_id} to path: {file_path}")
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f'Download {int(status.progress() * 100)}%.')
   
    fh.close()

def update_flag_file(flag_file_id, value):
    print(f"Updating flag file ID: {flag_file_id} with value: {value}")
    # Create a temporary file to store the flag value
    with open('flag_temp.txt', 'w') as temp_file:
        temp_file.write(str(value))
    media = MediaFileUpload('flag_temp.txt', mimetype='text/plain')
    file = service.files().update(fileId=flag_file_id, media_body=media).execute()
    print(f'Flag file updated: {file.get("id")}')

def get_file_content(file_id):
    print(f"Getting content of file ID: {file_id}")
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read().decode('utf-8')
   
def get_file_id_by_name(file_name, folder_id):
    print(f"Retrieving file ID for file name: {file_name} in folder ID: {folder_id}")
    query = f"name = '{file_name}' and '{folder_id}' in parents"
    results = service.files().list(
        q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print(f"No file named {file_name} found in folder ID: {folder_id}")
        return None
    else:
        file_id = items[0]['id']
        print(f"Found file ID: {file_id} for file name: {file_name}")
        return file_id