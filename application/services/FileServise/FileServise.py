import os
from datetime import datetime
import requests
from flask import request, render_template, send_from_directory, jsonify, redirect
from utils.timeit import timeit
from utils.json import read_json_file
from application.services.CrosReplica.Replica import send_files_to_servers


class FileService:

    def __init__(self, FileManager: object, Instence: object, Config: object, GeoLocator: object) -> None:
        self.file_manager = FileManager()
        self.instance = Instence()
        self.config = Config()
        self.geo_locator = GeoLocator()
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
        url = request.form.get('url')
        nearest_host = self.geo_locator.find_nearest_host(url)
        
        upload_response = self.get_uploading_attributes(url, nearest_host)
        is_origin_host = nearest_host == request.host_url

        task = send_files_to_servers.delay(is_origin_host, nearest_host, upload_response['filename'])
        print("task id:", task.id)

        return render_template("upload_info.html", response=upload_response) 
    

    def get_uploading_attributes(self, url: str, host: str):
        filename = url.split('/')[-1]
        response = requests.get(url, stream=True)

        download_link = f"{host}download/{filename}"

        if host == request.host_url:
            upload_folder = self.config.get_upload_folder()
            duration = self.file_manager.write_file(upload_folder, filename, response)
            data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _, duration = duration
            upload_response = {"data_time":data_time, "duration": duration, "instance_data": self.instance.get_instance_data()}
        else:
            upload_endpoint = self.config.get_upload_file_endpoint()
            upload_response = self.file_manager.upload_file(host, upload_endpoint, filename, response)

        upload_response['duration'] = str(upload_response['duration'])[:6]
        upload_response['filename'] = filename
        upload_response['download_link'] = download_link

        return upload_response


    def uploads(self):
        upload_folder = self.config.get_upload_folder()
        self.file_manager.assert_existing_folder(upload_folder)
        files = self.file_manager.load_uploads(upload_folder)
        return render_template("uploads.html",files=files)
    
    def download(self, file: str):
        return send_from_directory(self.config.get_upload_folder(), file, as_attachment=True) 
    

    def download_redirection(self, file):
        client_ip_address = request.remote_addr
        print('client_ip_address', client_ip_address)
        nearest_host = self.geo_locator.find_nearest_host(client_ip_address)
        return redirect(f'{nearest_host}download-info/{file}')


    def download_info(self, file: str):
        uploads_folder = self.config.get_upload_folder()

        if not self.file_manager.assert_file_existing(uploads_folder, file):
            return render_template('download404.html', file=file)
        
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

        if not self.file_manager.assert_file_existing(replica_folder, file, extension='.json'):
            return render_template('replica404.html', filename=file)
        
        replicas = read_json_file(replica_folder, file)
        replicas = replicas.get(file)

        return render_template('replica.html',replicas=replicas, filename=file)
        
            

