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
        self.assert_project_folder()


    def assert_project_folder(self):
        upload_folder = self.config.get_upload_folder()
        replica_folder = self.config.get_replica_folder()

        self.file_manager.assert_existing_folder(upload_folder)
        self.file_manager.assert_existing_folder(replica_folder)


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
        host = 'http://192.168.1.2/'
    
        response, upload_response = self.get_uploading_attributes(host)

        is_origin_host = host == request.host_url
        self.write_replica.replicate(is_origin_host, host, response, upload_response['filename'])

        return render_template("upload_info.html", response=upload_response) 
    

    def get_uploading_attributes(self, host: str):
        url = request.form['url']
        filename = url.split('/')[-1]
        response = requests.get(url, stream=True)

        upload_endpoint = self.config.get_upload_file_endpoint()
        self.file_manager.upload_file(host, upload_endpoint, filename, response)

        download_link = f"{request.host_url}download/{filename}"

        if host == request.host_url:
            upload_folder = self.config.get_upload_folder()
            duration = self.file_manager.write_file(upload_folder, filename, response)
            data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _, duration = duration
            upload_response = {"data_time":data_time, "duration": duration, "instance_data": self.instance.get_instance_data()}
        else:
            upload_endpoint = self.config.get_upload_file_endpoint()
            upload_response = self.file_manager.upload_file(host, upload_endpoint, filename, response)
        
        upload_response['filename'] = filename
        upload_response['download_link'] = download_link

        return response, upload_response


    def uploads(self):
        upload_folder = self.config.get_upload_folder()
        self.file_manager.assert_existing_folder(upload_folder)
        files = self.file_manager.load_uploads(upload_folder)
        return render_template("uploads.html",files=files)
    
    def download(self, file: str):
        return send_from_directory(self.config.get_upload_folder(), file, as_attachment=True) 
    

    def download_info(self, file: str):
        instance_data = self.instance.get_instance_data()
        return render_template('download.html', instance_data=instance_data, filename=file)
    
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
        
            

