from flask_app.models import *
from flask_app.decorators import *
#from models import *
from flask import Flask, render_template
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import random
import string
from hashlib import sha512

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config.from_pyfile('config/config_db.py')
app.config.from_pyfile('config/config_security.py')
app.config.from_pyfile('config/config_mail.py')
app.config['SECRET_KEY'] = 'super-secret'
oauth = OAuth2Provider(app)
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Gameplan API',
          description='Gameplan web and mobile app REST API',
          contact='gameplandev@gmail.com'
          )
mailer = Mail(app)
SIMPLE_CHARS = string.ascii_letters + string.digits


@api.route('/hello-<string:name>', endpoint='/hello')
class Hello(Resource):
    def get(self, name):
        return 'Hello, {0}!'.format(name)

@oauth.require_oauth()
@api.route('/user-<int:id>')
class User(Resource):
    @api.doc(description='Get a user by their ID')
    @api.marshal_with(Users.modelJson(api))
    def get(self, id):
        user = db.session.query(Users).filter_by(id=id).first()
        return user

@oauth.require_oauth()
@api.route('/add')
class Add(Resource):
    @api.doc(description='Add a new user to the database')
    @api.marshal_with(Users.modelJson(api))
    @api.expect(Users.modelPost(api), validate=True)
    def post(self):
        args = Users.req().parse_args(strict=True)
        user = Users(None,args['first'],args['last'],None,args['email'],args['role'],args['schoolid'],args['addressid'],None,None)
        db.session.add(user)
        db.session.commit()
        validator = Validators(user.id, randomString(), None)
        db.session.add(validator)
        db.session.commit()

        msg = Message("Welcome to Gameplan")
        msg.add_recipient(user.email)
        msg.html = render_template('alert.html', first=user.first, last=user.last, school='Some Random High School',
                                   validator=validator.validator)
        mailer.send(msg)
        print('sent {0}'.format(user.id))
        return user


@api.route('/validator-<string:v>')
class Validator(Resource):
    @api.doc(description='Get the user connected to the validator')
    @api.marshal_with(Users.modelJson(api))
    def get(self, v):
        validator = db.session.query(Validators).filter_by(validator=v).first()
        user = db.session.query(Users).filter_by(id=validator.userid).first()
        return user

@api.route('/oauth/authorize')
@login_required
@oauth.authorize_handler
class Authorize():
    @api.expect(Users.modelPost(api), validate=True)
    def get(self):
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

    def post(self):
        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'

@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None

@app.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass


def randomString(length=32):
    return ''.join(random.choice(SIMPLE_CHARS) for i in range(length))


def randomHash(length=32):
    hash = sha512()
    hash.update(randomString())
    return hash.hexdigest()[:length]


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        scopes=' '.join(request.scopes),
        user=get_current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(None, request.client.client_id, request.user.id, token['token_type'], token['access_token'], token['refresh_token'], expires,
                token['scope']
    )
    db.session.add(tok)
    db.session.commit()
    return tok

@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = Users.query.filter_by(username=username).first()
    if user.check_password(password):
        return user
    return None


if __name__ == '__main__':
    app.run()
