from __init__ import app
from application.services.FileServise.FileServise import FileService


file_service = FileService()

app.add_url_rule(
    rule="/", methods=["GET"], view_func=file_service.start_page)

app.add_url_rule(
    rule="/download", methods=["POST"], view_func=file_service.download)
