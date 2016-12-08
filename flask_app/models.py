# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, String, text, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_restplus import fields, reqparse

Base = declarative_base()
metadata = Base.metadata

class Addresses(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    line1 = Column(String(100), nullable=False)
    line2 = Column(String(100))
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)


class Auths(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    userid = Column(Integer, nullable=False, unique=True)
    created = Column(DateTime, nullable=False)
    oauthtoken = Column(String(64), nullable=False, unique=True)
    refreshtoken = Column(String(64), nullable=False, unique=True)
    expiration = Column(DateTime, nullable=False)


class Brags(Base):
    __tablename__ = 'brag'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    authorid = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    media = Column(String(64))
    body = Column(String(512))
    categoryid = Column(Integer)
    approverid = Column(Integer)


class Categories(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    type = Column(String(1), nullable=False)

class Client(Base):
    __tablename__ = 'client'

    id = Column(String(50), primary_key=True, unique=True)
    secret = Column(String(64), nullable=False, unique=True)
    name = Column(String(40))
    userid = Column(Integer, nullable=False)
    confidential = Column(Boolean, nullable=False)
    redirect_uris = Column(Text)
    default_scopes = Column(Text)

    @property
    def client_type(self):
        if self.confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self.redirect_uris:
            return self.redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scopes:
            return self.default_scopes.split()
        return []


class Connections(Base):
    __tablename__ = 'connection'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    userid1 = Column(Integer, nullable=False)
    userid2 = Column(Integer, nullable=False)
    status = Column(String(1))
    actionid = Column(Integer)


class Gameplans(Base):
    __tablename__ = 'gameplan'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    categoryid = Column(Integer, nullable=False)
    body = Column(String(512), nullable=False)
    status = Column(String(1))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime)


class Grant(Base):
    __tablename__ = 'grant'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    clientid = Column(String(50), nullable=False)
    code = Column(String(255), nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    scopes = Column(Text)

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self.scopes:
            return self.scopes.split()
        return []


class Ratings(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    gameplanid = Column(Integer, nullable=False)
    score = Column(Float)
    created = Column(DateTime)


class Schools(Base):
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    adminid = Column(Integer, nullable=False)
    addressid = Column(Integer, nullable=False)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    clientid = Column(String(50), nullable=False)
    userid = Column(Integer)
    token_type = Column(String(40))
    accesstoken = Column(String(255), unique=True)
    refreshtoken = Column(String(255), unique=True)
    expires = Column(DateTime)
    scopes = Column(Text)

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self.scopes:
            return self.scopes.split()
        return []


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    first = Column(String(64), nullable=False)
    last = Column(String(64), nullable=False)
    username = Column(String(100), unique=True)
    email = Column(String(120), nullable=False, unique=True)
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

    def modelJson(api):
        userModel = api.model('User', {
            'id': fields.Integer,
            'first': fields.String,
            'last': fields.String,
            'username': fields.String,
            'email': fields.String,
            'role': fields.String,
            'schoolid': fields.Integer,
            'addressid': fields.Integer,
            'created': fields.DateTime,
            'joined': fields.DateTime
        })
        return userModel

    def modelPost(api):
        newUserModel = api.model('New User', {
            'first': fields.String,
            'last': fields.String,
            'email': fields.String,
            'role': fields.String,
            'schoolid': fields.Integer,
            'addressid': fields.Integer,
        })
        return newUserModel

    @staticmethod
    def req():
        userParser = reqparse.RequestParser()
        userParser.add_argument('first', type=str, help='First name required')
        userParser.add_argument('last', type=str, help='Last name required')
        userParser.add_argument('email', type=str, help='Email address required')
        userParser.add_argument('role', type=str, help='Role required (A=admin, S=student, T=teacher, P=parent')
        userParser.add_argument('schoolid', type=int, help='School ID required')
        userParser.add_argument('addressid', type=int, help='Address ID required')
        return userParser


class Validators(Base):
    __tablename__ = 'validator'

    userid = Column(Integer, primary_key=True, unique=True)
    validator = Column(String(32), nullable=False, unique=True, server_default=text("now()"))
    created = Column(DateTime, nullable=False, server_default=text("now()"))

    def __init__(self, userid, validator, date):
        self.userid = userid
        self.validator = validator
        self.created = date

