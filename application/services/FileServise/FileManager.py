import os
import time
from __init__ import app
import requests
from utils.timeit import timeit


class FileManager:

    def assert_existing_folder(self, folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def assert_file_existing(self, folder_name: str, file: str):
        if os.path.isfile(f'{folder_name}/{file}.json'):
            return True
        

    @timeit
    def write_file(self, folder_name: str, file_name: str, response: object):
        with open(f'{folder_name}/{file_name}', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def upload_file(self, host: str, endpoint:str, file_name: str, response: bytes):
        files = {'file': (file_name, response.content)}
        target_url = host + endpoint
        res = requests.post(target_url, files=files)
        return res.text
        

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

