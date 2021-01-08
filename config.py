import os
import yaml
from datetime import timedelta

# Enable or disable development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# db config
db_config = yaml.load(open('db_config/cleardb.yaml'), Loader=yaml.FullLoader)

db_host = db_config['mysql_host']
db_user = db_config['mysql_user']
db_password = db_config['mysql_password']
db_name = db_config['mysql_db']

# SQLAlchemy config
SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'max_overflow': 0,
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# JWT config
JWT_AUTH_USERNAME_KEY = 'email'
JWT_AUTH_URL_RULE = '/api/auth/'
JWT_EXPIRATION_DELTA = timedelta(days=60)

# Secret key for signing things
SECRET_KEY = b'd092b96b4edff56c1843aa87e0b1341b46310d4826c53a21'