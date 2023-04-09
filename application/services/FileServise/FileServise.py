from __init__ import app
from flask import request, render_template, send_file


class FileService:


    def upload(self):
        return render_template("upload.html")
    
    def upload_info(self):
        return render_template(
            "upload_info.html",
            instance_id='12345',
            instance_ip='170.10.0.1',
            instance_location='Frankfurt',
            upload_duration='12',
            upload_time='2023-01-11 10:00:020',
            download_link='http:12345'
            )

