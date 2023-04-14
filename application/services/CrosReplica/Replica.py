import json
import requests
from flask import request
from __init__ import celery
from application.services.FileServise.FileManager import FileManager
from utils.config import Config
from utils.json import write_json_to_file


class FileReplica:

    def __init__(self) -> None:
        self.config = Config()
        self.file_manager = FileManager()
    

    def get_hosts_for_replication(self, host: str):       
        hosts = self.config.get_available_hosts()
        if host in hosts: hosts.remove(host)

        return hosts

        
    def send_files_to_servers(self, filename: str, host: str) -> list[dict]:
        hosts = self.get_hosts_for_replication(host)
        upload_folder = self.config.get_upload_folder()
        upload_endpoint = self.config.get_upload_file_endpoint()
        
        responses = []
        for host in hosts:
            response = self.file_manager.upload_file_from_local(host, upload_endpoint, upload_folder, filename)
            responses.append(response.text)

        return responses
    
    
    def write_replicas_info(self, filename: str, responses: list[dict]) -> None:
        replica_folder = self.config.get_replica_folder()
        replicas = [json.loads(response) for response in responses]
        write_json_to_file(replica_folder, filename, {filename: replicas })


    def replicate_file(self, filename: str, host='') -> dict:
        host = self.assert_host_for_call(host)
        replica_responses = self.send_files_to_servers(filename, host)
        self.write_replicas_info(filename, replica_responses)

        return {"massage": f"File: {filename} was replicated"}


    def assert_host_for_call(self, host='') -> str:
        try:
            host = request.host_url
        except Exception as e:
            print("It is not reqeust", e)
        finally:
            host = host

        return host

                     
    
@celery.task()
def send_files_to_servers(is_origin_host: bool, host: str, filename: str):    
    if is_origin_host:
        file_replica = FileReplica()
        file_replica.replicate_file(filename, host)
    else:
        config = Config()
        replicate_file_endpoint = config.get_replicate_file_endpoint()
        url = f'{host}{replicate_file_endpoint}/{filename}' 
        requests.get(url)
        
    print('done replicate')
