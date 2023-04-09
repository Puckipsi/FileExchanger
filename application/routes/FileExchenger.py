from __init__ import app
from application.services.FileServise.FileServise import FileService
from application.services.FileServise.FileManager import FileManager
from application.services.FileServise.Instence import EC2Instance


file_service = FileService(FileManager, EC2Instance)

app.add_url_rule(
    rule="/", methods=["GET"], view_func=file_service.upload)

app.add_url_rule(
    rule="/upload-info", methods=["POST"], view_func=file_service.upload_info)