import asyncio
import aiohttp


class WriteReplica:

    async def upload_file(self, url, response, filename):
        data = aiohttp.FormData()
        data.add_field('file', response.content, filename=filename)
       
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                print("Replica ", url)
                if response.status != 200:
                    print("Faild to repliacte")
                return response.status, await response.text()
                

    async def upload_file_to_servers(self, response, server_urls, filename):
        tasks = []
        for url in server_urls:
            task = asyncio.create_task(self.upload_file(url, response,filename))
            tasks.append(task)
        await asyncio.gather(*tasks)


    def replicate(self, response, hosts, filename):
        asyncio.run(self.upload_file_to_servers(response, hosts, filename))
        
