from flask import Flask


app = Flask(__name__, 
            template_folder='application/templates',
            static_folder='application/static')


import application.routes