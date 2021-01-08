from flask import Flask
from flask_cors import CORS
import sys
import logging

def create_app():
    from . import routes, models

    app = Flask(__name__)
    app.config.from_object('config')

    routes.init_app(app)
    models.init_app(app)

    CORS(app)

    return app