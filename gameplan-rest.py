from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
#from models import Users
from sqlalchemy import Column, DateTime, Float, Integer, String, text

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Gameplan API',
          description='Gameplan web and mobile app REST API',
          contact='gameplandev@gmail.com',
          )

userModel = api.model('User', {
    'id': fields.Integer,
    'first': fields.String,
    'last': fields.String,
    'username': fields.String,
    'email': fields.String,
    'role': fields.String,
    'schoolID': fields.String,
    'addressID': fields.String,
    'created': fields.String,
    'joined': fields.String
})

class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    first = Column(String(64), nullable=False)
    last = Column(String(64), nullable=False)
    username = Column(String(100), unique=True)
    email = Column(String(120), nullable=False)
    role = Column(String(1), nullable=False)
    schoolid = Column(Integer, nullable=False)
    addressid = Column(Integer)
    hash = Column(String(64))
    salt = Column(String(16))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    joined = Column(DateTime)

    def __init__(self, id, first, last, username, email, role, schoolId, addressId, created, joined):
        self.id = id
        self.first = first
        self.last = last
        self.username = username
        self.email = email
        self.role = role
        self.schoolid = schoolId
        self.addressid = addressId
        self.created = created
        self.joined = joined

    def modelJson(self, api):
        userModel = api.model('User', {
            'id': fields.Integer,
            'first': fields.String,
            'last': fields.String,
            'username': fields.String,
            'email': fields.String,
            'role': fields.String,
            'schoolID': fields.String,
            'addressID': fields.String,
            'created': fields.String,
            'joined': fields.String
        })
        return userModel


@api.route('/user-<int:id>')
class User(Resource):
    @api.marshal_with(userModel)
    def get(self, id):
        user = Users.query.filter_by(id=id).first()
        return user


@api.route('/validator-<string:validator>')
class Validator(Resource):
    def get(self, validator):
        return {'user': validator}


if __name__ == '__main__':
    app.run()
