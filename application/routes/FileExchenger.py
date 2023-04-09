from __init__ import app
from application.services.FileServise.FileServise import FileService


file_service = FileService()

app.add_url_rule(
    rule="/", methods=["GET"], view_func=file_service.upload)

app.add_url_rule(
    rule="/upload-info", methods=["POST"], view_func=file_service.upload_info)
