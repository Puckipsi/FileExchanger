import asyncio
import aiohttp
import aiofiles
import requests
import json
from utils.json import write_json_to_file
from utils.config import Config


class WriteReplica:

    def  __init__(self) -> None:
        self.config = Config()


    async def upload_file(self, is_origin, host, response, upload_folder, upload_endpoint, filename):
        data = aiohttp.FormData()

        async with aiohttp.ClientSession() as session:
            if is_origin:
                async with aiofiles.open(f'{upload_folder}/{filename}', 'rb') as f:
                    file_content = await f.read()
                    data.add_field('file', file_content, filename=filename)
                    print("Replica from file", host)
                    async with session.post(host + upload_endpoint, data=data) as response:
                        if response.status != 200:
                            print("Faild to repliacte", response)
                        return await response.text()
                  
            data.add_field('file', response.content, filename=filename)
            async with session.post(host + upload_endpoint, data=data) as response:
                print("Replica from response", host)
                if response.status != 200:
                    print("Faild to repliacte")
                return await response.text()
            
    
    async def upload_file_to_servers(self, is_origin, response, hosts, filename):
        tasks = []
        replica_folder = self.config.get_replica_folder()
        upload_folder = self.config.get_upload_folder()
        upload_endpoint = self.config.get_upload_file_endpoint()

        for host in hosts:
            upload = self.upload_file(is_origin, host, response, upload_folder, upload_endpoint, filename)
            task = asyncio.create_task(upload)
            tasks.append(task)

        response = await asyncio.gather(*tasks)
        replicated = [json.loads(res) for res in response]
        write_json_to_file(replica_folder, filename, {filename:replicated })

    
    def replicate(self, is_origin, host, response, filename):
        hosts = self.config.get_available_hosts()
        hosts.remove(host)
        asyncio.run(self.upload_file_to_servers(is_origin, response, hosts, filename))
        
