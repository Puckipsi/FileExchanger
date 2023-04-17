import os
import time
import json
from __init__ import app
import requests
from datetime import datetime
from utils.config import Config
import pytz


config = Config()


class FileManager:

    def assert_existing_folder(self, folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def assert_file_existing(self, folder_name: str, file: str, extension: str=''):
        if os.path.isfile(f'{folder_name}/{file}{extension}'):
            return True
        

    def write_file(self, url: str, folder_name: str, file_name: str):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(f'{folder_name}/{file_name}', 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    
    def redirecting_upload_to_nearest_host(self, host: str, upload_info_endpoint: str, download_url: str):
        data = {'url': download_url}
        with requests.post(host + upload_info_endpoint, data=data) as response:
            response.raise_for_status()

        return response.text


    def upload_file_from_local(self, host: str, upload_endpoint:str, upload_folder: str, filename: str):
        with open(f'{upload_folder}/{filename}', 'rb') as file:
            while True:
                chunk = file.read(1024*1024) #1mb
                if not chunk:
                    break
                files = {'file': (filename, chunk)}
                response = requests.post(host + upload_endpoint, files=files, timeout=5)
                response.raise_for_status()

        return response
        

    def load_uploads(self, upload_folder: str):
        time_zone = pytz.timezone(config.get_time_zone())
        dir_path = os.path.join(app.root_path, upload_folder)
        dir_files = os.listdir(dir_path)
        files = []

        for file in sorted(dir_files):
            file_path = f"{dir_path}/{file}"
            last_modified_time = datetime.utcfromtimestamp(os.path.getmtime(file_path))
            last_modified_time = time_zone.localize(last_modified_time).astimezone(time_zone)
            files.append({
                'file': file,
                "size": os.path.getsize(file_path),
                'upload_date': last_modified_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            })
        
        return files
    
    def get_file_path(self, folder_name: str, file: str):
        file_path = os.path.join(app.root_path, folder_name, file)
        return file_path

