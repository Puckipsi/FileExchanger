from __init__ import app
from flask import request, render_template, send_file


class FileService:


    def start_page(self):
        return render_template("upload.html")
    
    def download(self):
        pass

