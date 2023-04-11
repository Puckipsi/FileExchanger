import os
from datetime import datetime
import requests
from __init__ import app
from flask import request, render_template, send_from_directory
from dotenv import dotenv_values
from utils.timeit import timeit


config = dotenv_values('.env')


class FileService:

    def __init__(self, FileManager: object, Instence: object) -> None:
        self.file_manager = FileManager()
        self.instance = Instence()

    def upload(self):
        return render_template("upload.html")
    
    def upload_info(self):
        folder = self.get_upload_folder()
        self.file_manager.assert_existing_folder(folder)

        file_attributes, duration =  self.get_uploading_attributes(folder)
        full_url, filename, date_time = file_attributes
        
        return render_template(
            "upload_info.html",
            vps_name=f'VPS-{self.instance.InstanceLocationRegion}',
            instance_id=self.instance.InstanceId,
            instance_ip=self.instance.InstancePublicIPv4,
            instance_location_region=self.instance.InstanceLocationRegion,
            upload_duration=f'{duration:.2f}',
            upload_date=date_time,
            download_link=full_url,
            filename = filename
            )         
    
    @timeit 
    def get_uploading_attributes(self, folder: str):
        url = request.form['url']
        file_name = url.split('/')[-1]
        response = requests.get(url, stream=True)
        self.file_manager.write_file(folder, file_name,  response)
        data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_path = f"{request.url_root}download/{file_name}"
        print('req from:',request.remote_addr)
        return full_path, file_name, data_time 


    def uploads(self):
        files = self.file_manager.load_uploads(self.get_upload_folder())
        return render_template("uploads.html",files=files)
    
    def download(self, file: str):
        return send_from_directory(config['UPLOAD_FOLDER'], file, as_attachment=True) 
    

    def download_info(self, file: str):
        return render_template('download.html', filename=file)
    
    def remove(self, file):
        file_path = self.file_manager.get_file_path(self.get_upload_folder(), file)

        try:
            os.remove(file_path)
        except Exception as e:
            print("An error occurred while removing file", e)
        finally:
            return self.uploads()
        
    
    def get_upload_folder(self):
        return config['UPLOAD_FOLDER']
    


