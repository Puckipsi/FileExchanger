import asyncio
import aiohttp
import json
from utils.json import write_json_to_file

class WriteReplica:

    async def upload_file(self, url, response, upload_endpoint, filename):
        data = aiohttp.FormData()
        data.add_field('file', response.content, filename=filename)

        async with aiohttp.ClientSession() as session:
            async with session.post(url+upload_endpoint, data=data) as response:
                print("Replica ", url)
                if response.status != 200:
                    print("Faild to repliacte")
                return await response.text()
                

    async def upload_file_to_servers(self, response, server_urls, upload_endpoint, filename):
        tasks = []
        for url in server_urls:
            upload = self.upload_file(url, response, upload_endpoint, filename)
            task = asyncio.create_task(upload)
            tasks.append(task)
            
        response = await asyncio.gather(*tasks)
        replicated = [json.loads(res) for res in response]
        write_json_to_file(filename, {filename:replicated })


    def replicate(self, response, hosts, upload_endpoint, filename):
        asyncio.run(self.upload_file_to_servers(response, hosts, upload_endpoint, filename))
        
