from flask_app.models import *
#from models import *
from flask import Flask, render_template
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, auth_required
from flask_oauthlib.provider import OAuth2Provider
from flask_mail import Mail, Message

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
userDatastore = SQLAlchemyUserDatastore(db, Users, Users.role)
app.security = Security(app, userDatastore)
mailer = Mail(app)

@api.route('/hello-<string:name>', endpoint='/hello')
class Welcome(Resource):
    def get(self, name):
        return 'Hello, {0}!'.format(name)

@app.route('/welcome')
@login_required
def home():
    return render_template('index.php')

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

        msg = Message("Welcome to Gameplan")
        msg.add_recipient(user.email)
        msg.html = '<p>Hello, {0} {1}</p>' \
                   '<p>Click the link below to activate your account.</p>' \
                   '<a href="http://ec2-54-160-178-89.compute-1.amazonaws.com">Gameplan.com</a>' \
                   '<p>Thanks,</p>' \
                   '<p>Cash</p>'.format(user.first, user.last)
        print('sending {0}'.format(user.first))
        mailer.send(msg)

        return user

@api.route('/validator-<string:validator>')
class Validator(Resource):
    def get(self, validator):
        return {'user': validator}


if __name__ == '__main__':
    app.run()
