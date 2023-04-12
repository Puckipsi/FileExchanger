from dotenv import dotenv_values


config = dotenv_values('.env')


class Config:
    
    def get_upload_folder(self):
        return config['UPLOAD_FOLDER']
    

    def get_upload_file_endpoint(self):
        return config['UPLOAD_FILE_ENDPOINT']
    

    def get_available_hosts(self):
        return config['AVAILABLE_HOSTS'].split(',')