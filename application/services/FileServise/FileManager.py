import os
import time
from __init__ import app


class FileManager:

    def assert_existing_folder(self, folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)


    def write_file(self, folder_name: str, file_name: str, content: bytes):
        with open(f'{folder_name}/{file_name}', 'wb') as f:
            f.write(content)

