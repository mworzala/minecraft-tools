
import os
import zipfile
import requests

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"Error: Unable to fetch file {filename} (status code: {response.status_code})")
        return False
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return True

def extract_zip_archive(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(filename))