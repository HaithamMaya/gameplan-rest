from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
from flasgger import Swagger
import os

app = Flask(__name__)

script = os.getcwd().split('/')[-1]
print('running: ',script)

if script == 'flask_tests':
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config.from_pyfile('test_config/test_config_db.py')
    app.config.from_pyfile('test_config/test_config_security.py')
    app.config.from_pyfile('test_config/test_config_mail.py')
    app.config.from_pyfile('test_config/test_config_swagger.py')
else:
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config.from_pyfile('config/config_db.py')
    app.config.from_pyfile('config/config_security.py')
    app.config.from_pyfile('config/config_mail.py')
    app.config.from_pyfile('config/config_swagger.py')

db = SQLAlchemy(app)
oauth = OAuth2Provider(app)
Swagger(app)

HOME_URL = "http://api.mygameplan.io/"
ENCRYPTION_METHOD = 'pbkdf2:sha1'

from flask_app.routes import *
from flask_app.oauth2 import *

if __name__ == '__main__':
    app.run()