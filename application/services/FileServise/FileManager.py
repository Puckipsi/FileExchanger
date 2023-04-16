import os
import time
import json
from __init__ import app
import requests


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
            files = {'file': (filename, file)}
            response = requests.post(host + upload_endpoint, files=files)

        return response
        

    def load_uploads(self, upload_folder: str):
        dir_path = os.path.join(app.root_path, upload_folder)
        dir_files = os.listdir(dir_path)
        files = [{
		    'file': file,
            "size": os.path.getsize(f"{dir_path}/{file}"),
	        'upload_date': time.ctime(os.path.getctime(f"{dir_path}/{file}"))} for file in sorted(dir_files)]  
        
        return files
    
    def get_file_path(self, folder_name: str, file: str):
        file_path = os.path.join(app.root_path, folder_name, file)
        return file_path

