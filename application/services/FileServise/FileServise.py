import os
from datetime import datetime
import requests
from __init__ import app
from flask import request, render_template, send_from_directory
from utils.timeit import timeit



class FileService:

    def __init__(self, FileManager: object, Instence: object, WriteReplica: object, Config: object) -> None:
        self.file_manager = FileManager()
        self.instance = Instence()
        self.write_replica = WriteReplica()
        self.config = Config()

    def upload(self):
        return render_template("upload.html")
    
    def upload_file(self):
        folder = self.config.get_upload_folder()
        file = request.files['file']
        filename = file.filename
        file.save("/".join((folder, filename)))

        #file = request.files["file"]
        #filename = file.filename
        #folder = self.config.get_upload_folder()
        #file.save("/".join((folder, filename)))
        return 'File uploaded successfully'
    
    
    def upload_info(self):
        self.file_manager.assert_existing_folder(self.config.get_upload_folder())
        host = 'http://192.168.1.2/'
        urls = self.config.get_available_hosts()

        upload_endpoint = self.config.get_upload_file_endpoint()
        file_attributes, duration =  self.get_uploading_attributes(host, upload_endpoint)
        full_url, filename, date_time, response = file_attributes
 
        self.write_replica.replicate(response, urls, filename)
        
        return render_template(
            "upload_info.html",
            vps_name=f'VPS-{self.instance.InstanceLocationRegion}',
            instance_id=self.instance.InstanceId,
            instance_ip=self.instance.InstancePublicIPv4,
            instance_location_region=self.instance.InstanceLocationRegion,
            upload_duration=f'{duration:.4f}',
            upload_date=date_time,
            download_link=full_url,
            filename = filename
            ) 
    
    @timeit 
    def get_uploading_attributes(self, host: str, endpoint: str,):
        url = request.form['url']
        file_name = url.split('/')[-1]
        response = requests.get(url, stream=True)
        self.file_manager.upload_file(host, endpoint, file_name, response)
        data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_path = f"{host}download/{file_name}"
        
        return full_path, file_name, data_time, response


    def uploads(self):
        files = self.file_manager.load_uploads(self.config.get_upload_folder())
        return render_template("uploads.html",files=files)
    
    def download(self, file: str):
        return send_from_directory(self.config.get_upload_folder(), file, as_attachment=True) 
    

    def download_info(self, file: str):
        return render_template('download.html', filename=file)
    
    def remove(self, file):
        file_path = self.file_manager.get_file_path(self.config.get_upload_folder(), file)
        print(file_path)
        try:
            os.remove(file_path)
        except Exception as e:
            print("An error occurred while removing file", e)
        finally:
            return self.uploads()
        

