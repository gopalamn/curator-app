from .test import test
from flask_jwt import JWT

def init_app(app):
    app.register_blueprint(test)
