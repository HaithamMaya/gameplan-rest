import sys
from flask import Flask, request
from flask_restplus import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_app.models import *

sys.path.insert(0, './')

app = Flask(__name__)
app.config.from_pyfile('config_app.py')
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Gameplan API',
          description='Gameplan web and mobile app REST API',
          contact='gameplandev@gmail.com',
          )

userParser = reqparse.RequestParser()
userParser.add_argument('first', type=str, help='First name required')
userParser.add_argument('last', type=str, help='Last name required')
userParser.add_argument('email', type=str, help='Email address required')
userParser.add_argument('role', type=str, help='Role required (A=admin, S=student, T=teacher, P=parent')
userParser.add_argument('schoolid', type=int, help='School ID required')
userParser.add_argument('addressid', type=int, help='Address ID required')

@api.doc('Hello, World!')
@api.route('/hello-<string:name>', endpoint='/hello')
class Welcome(Resource):
    def get(self, name):
        return 'Hello, {0}!'.format(name)

@api.route('/user-<int:id>')
class User(Resource):
    @api.doc(summary='Get User', description='Get a user by their ID')
    @api.marshal_with(Users.modelJson(api))
    def get(self, id):
        user = db.session.query(Users).filter_by(id=id).first()
        return user

@api.route('/add')
class Add(Resource):
    @api.doc(summary='Add User', description='Add a new user to the database')
    @api.marshal_with(Users.modelJson(api))
    @api.expect(Users.modelPost(api), validate=True)
    def post(self):
        args = userParser.parse_args(strict=True)
        user = Users(None,args['first'],args['last'],None,args['email'],args['role'],args['schoolid'],args['addressid'],None,None)
        db.session.add(user)
        db.session.commit()
        return user

@api.route('/validator-<string:validator>')
class Validator(Resource):
    def get(self, validator):
        return {'user': validator}


if __name__ == '__main__':
    app.run(debug=True)
