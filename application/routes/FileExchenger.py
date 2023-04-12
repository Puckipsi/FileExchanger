from __init__ import app
from application.services.FileServise.FileServise import FileService
from application.services.FileServise.FileManager import FileManager
from application.services.FileServise.Instence import EC2Instance
from application.services.CrosReplica.WriteReplica import WriteReplica
from utils.config import Config


file_service = FileService(FileManager, EC2Instance, WriteReplica, Config)

app.add_url_rule(
    rule="/", methods=["GET"], view_func=file_service.upload)

app.add_url_rule(
    rule="/upload-info", methods=["POST"], view_func=file_service.upload_info)


app.add_url_rule(
    rule="/upload-file", methods=["POST"], view_func=file_service.upload_file)


app.add_url_rule(
    rule="/uploads", methods=["GET"], view_func=file_service.uploads)


app.add_url_rule(
    rule="/download/<file>", methods=["GET"], view_func=file_service.download)


app.add_url_rule(
    rule="/download-info/<file>", methods=["GET"], view_func=file_service.download_info)


app.add_url_rule(
    rule="/remove/<file>", methods=["GET"], view_func=file_service.remove)


