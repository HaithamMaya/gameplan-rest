from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config.from_pyfile('config/config_db.py')
app.config.from_pyfile('config/config_security.py')
app.config.from_pyfile('config/config_mail.py')
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)

import flask_app.flaskapp