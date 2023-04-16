from dotenv import dotenv_values


config = dotenv_values('.env')


class Config:
    
    def get_upload_folder(self):
        return config['UPLOAD_FOLDER']
    
    def get_replica_folder(self):
        return config['REPLICA_FOLDER']
    

    def get_upload_file_endpoint(self):
        return config['UPLOAD_FILE_ENDPOINT']
    
    def get_upload_info_endpoint(self):
        return config['UPLOAD_INFO_ENDPOINT']
    
    def get_replicate_file_endpoint(self):
        return config['REPLICATE_FILE_ENDPOINT']

    def get_available_hosts(self):
        return config['AVAILABLE_HOSTS'].split(',')
    
    def get_time_zone(self):
        return config['TIME_ZONE']