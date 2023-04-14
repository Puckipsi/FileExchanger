from flask import Flask
from celery import Celery
from utils.celery import get_celery_app_instance



app = Flask(__name__, 
            template_folder='application/templates',
            static_folder='application/static')

celery = get_celery_app_instance(app)

import application.routes