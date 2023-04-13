import os
from datetime import datetime
import requests
from flask import request, render_template, send_from_directory, jsonify
from utils.timeit import timeit
from utils.json import read_json_file
from __init__ import app

class FileService:

    def __init__(self, FileManager: object, Instence: object, WriteReplica: object, Config: object) -> None:
        self.file_manager = FileManager()
        self.instance = Instence()
        self.write_replica = WriteReplica()
        self.config = Config()

    def upload(self):
        return render_template("upload.html")
    
    def upload_file(self):
        data_time, duration = self.handle_upload()
        instance_data = self.instance.get_instance_data()
        return jsonify({'duration':f'{duration:.4f}', "data_time": data_time,"instance_data": instance_data})
        
    @timeit
    def handle_upload(self):
        folder = self.config.get_upload_folder()
        file = request.files['file']
        filename = file.filename
        file.save("/".join((folder, filename)))
        data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data_time
    
    
    def upload_info(self):
        upload_folder, replica_folder = self.config.get_upload_folder(), self.config.get_replica_folder()
        self.file_manager.assert_existing_folder(upload_folder)
        self.file_manager.assert_existing_folder(replica_folder)

        host = 'http://18.157.163.62/'
        urls = self.config.get_available_hosts()

        upload_endpoint = self.config.get_upload_file_endpoint()
        file_attributes, duration =  self.get_uploading_attributes(host, upload_endpoint)
        full_url, filename, date_time, response = file_attributes
 
        self.write_replica.replicate(replica_folder, response, urls, upload_endpoint, filename)
        instance_data = self.instance.get_instance_data()
        
        return render_template(
            "upload_info.html",
            vps_name='VPS-'+instance_data.get('instance_location_region'),
            instance_id=instance_data.get('instance_id'),
            instance_ip=instance_data.get('instance_public_ipv4'),
            instance_location_region=instance_data.get('instance_location_region'),
            upload_duration=f'{duration:.4f}',
            upload_date=date_time,
            download_link=full_url,
            filename = filename
            ) 
    
    @timeit 
    def get_uploading_attributes(self, host: str, endpoint: str,):
        url = request.form['url']
        file_name = url.split('/')[-1]
        print("geting req")
        response = requests.get(url, stream=True)
        print("post req")
        self.file_manager.upload_file(host, endpoint, file_name, response)
        data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        full_path = f"{request.host_url}download/{file_name}"
        
        return full_path, file_name, data_time, response


    def uploads(self):
        upload_folder = self.config.get_upload_folder()
        self.file_manager.assert_existing_folder(upload_folder)
        files = self.file_manager.load_uploads(upload_folder)
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
           
    def replica_info(self, file):
        replica_folder = self.config.get_replica_folder()

        if not self.file_manager.assert_file_existing(replica_folder, file):
            return render_template('replica404.html', filename=file)
        
        replicas = read_json_file(replica_folder, file)
        replicas = replicas.get(file)

        return render_template('replica.html',replicas=replicas, filename=file)
        
            

