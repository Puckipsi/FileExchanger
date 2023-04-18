import os
from flask import request, render_template, send_from_directory, jsonify, redirect
from utils.timeit import timeit, current_data_time
from utils.json import read_json_file
from utils.url import is_valid_url
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
        data_time = current_data_time()
        return data_time
    
    
    def upload_info(self):
        url = request.form.get('url')
        print("download url: ", url )
        url_validator = is_valid_url(url)
        if not url_validator.get('valid'):
            message = url_validator.get('message')
            return render_template('invalid_url.html', message=message)

        nearest_host = self.geo_locator.find_nearest_host(url)
        is_origin_host = nearest_host == request.host_url
        
        if is_origin_host:
            upload_response, duration  = self.get_uploading_attributes(url, nearest_host)
            upload_response['duration'] = str(duration)[:6]    
            task = send_files_to_servers.delay(nearest_host, upload_response['filename'])
            print("task id: ",task.id)
            return render_template("upload_info.html", response=upload_response)
        
        upload_info_response = self.config.get_upload_info_endpoint()
        response = self.file_manager.redirecting_upload_to_nearest_host(nearest_host, upload_info_response, url)
        
        return response
        

    @timeit
    def get_uploading_attributes(self, url: str, host: str) -> dict:
        filename = url.split('/')[-1]
        download_link = f"{host}download/{filename}"
        upload_folder = self.config.get_upload_folder()

        self.file_manager.write_file(url, upload_folder, filename)

        upload_response = {"data_time": current_data_time(),
                           "instance_data": self.instance.get_instance_data()}

        upload_response['filename'] = filename
        upload_response['download_link'] = download_link

        return upload_response


    def uploads(self):
        time_zone = self.config.get_time_zone()
        upload_folder = self.config.get_upload_folder()
        self.file_manager.assert_existing_folder(upload_folder)
        files = self.file_manager.load_uploads(upload_folder)
        return render_template("uploads.html",files=files, time_zone=time_zone)
    
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
        uploads_file_path = self.file_manager.get_file_path(self.config.get_upload_folder(), file)
        replica_file_path = self.file_manager.get_file_path(self.config.get_replica_folder(), file+'.json')

        try:
            os.remove(uploads_file_path)
            os.remove(replica_file_path)
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
    
    
    def logs(self):
        logs = self.file_manager.read_file('app.log')
        return render_template('logs.html', logs=logs)
        
            

