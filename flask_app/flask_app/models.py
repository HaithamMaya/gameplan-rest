from flask_app.__init__ import db
from sqlalchemy import Column, DateTime, Float, Integer, String, text, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_restplus import reqparse
from flask import jsonify

Base = declarative_base()


class Addresses(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    line1 = Column(String(100), nullable=False)
    line2 = Column(String(100))
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)

    def __init__(self, id, line1, line2, city, state, zip):
        self.id = id
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.state = state
        self.zip = zip


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

    client_id = Column(String(50), primary_key=True, unique=True)
    secret = Column(String(64), nullable=False, unique=True)
    name = Column(String(40))
    userid = Column(Integer, nullable=False)
    confidential = Column(Boolean, nullable=False)
    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    def __init__(self, id, secret, name, userid, confidential, redirects, scopes):
        self.client_id = id
        self.secret = secret
        self.name = name
        self.userid = userid
        self.confidential = confidential
        self._redirect_uris = redirects
        self._default_scopes = scopes

    @property
    def client_type(self):
        if self.confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self._redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Codes(Base):
    __tablename__ = 'code'

    six_digits = Column(String(6), primary_key=True, nullable=False, unique=True)
    expires = Column(DateTime)
    userid = Column(Integer, nullable=False)

    def __init__(self, six_digits, expires, userid):
        self.six_digits = six_digits
        self.expires = expires
        self.userid = userid

    @staticmethod
    def req():
        codeParser = reqparse.RequestParser()
        codeParser.add_argument('code', type=str, help='six-digit code required')
        codeParser.add_argument('userid', type=int, help='user id required')
        return codeParser


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
    user = Column(Integer, nullable=False)
    client_id = Column(String(50), nullable=False)
    code = Column(String(255), nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    _scopes = Column(String)

    def __init__(self, id, userid, clientid, code, redirect_uri, expires, scopes):
        self.id = id
        self.user = userid
        self.client_id = clientid
        self.code = code
        self.redirect_uri = redirect_uri
        self.expires = expires
        self._scopes = scopes

    @staticmethod
    def req():
        grantParser = reqparse.RequestParser()
        grantParser.add_argument('first', type=str, help='First name required')
        grantParser.add_argument('last', type=str, help='Last name required')
        grantParser.add_argument('email', type=str, help='Email address required')
        grantParser.add_argument('role', type=str, help='Role required (A=admin, S=student, T=teacher, P=parent')
        grantParser.add_argument('schoolid', type=int, help='School ID required')
        grantParser.add_argument('addressid', type=int, help='Address ID required')
        return grantParser

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
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

    def __init__(self, id, name, adminid, addressid):
        self.id = id
        self.name = name
        self.adminid = adminid
        self.addressid = addressid


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    client_id = Column(String(50), nullable=False)
    user = Column(Integer)
    token_type = Column(String(40))
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)

    def __init__(self, id, clientid, userid, token_type, accessToken, refreshToken, expires, scopes):
        self.id = id
        self.client_id = clientid
        self.user = userid
        self.token_type = token_type
        self.access_token = accessToken
        self.refresh_token = refreshToken
        self.expires = expires
        self._scopes = scopes

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    first = Column(String(64), nullable=False)
    last = Column(String(64), nullable=False)
    username = Column(String(100))
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

    def JSON(self):
        return jsonify({
            'id': self.id,
            'first': self.first,
            'last': self.last,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'schoolid': self.schoolid,
            'addressid': self.addressid,
            'created': self.created,
            'joined': self.joined
        })

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

    @staticmethod
    def reqLogin():
        loginParser = reqparse.RequestParser()
        loginParser.add_argument('username', type=str, help='username required')
        loginParser.add_argument('password', type=str, help='password required')
        return loginParser

    @staticmethod
    def reqUpdate():
        updateParser = Users.req()
        updateParser.add_argument('password', type=str, help='Password')
        updateParser.add_argument('username', type=str, help='Username')
        return updateParser


class Validators(Base):
    __tablename__ = 'validator'

    userid = Column(Integer)
    validator = Column(String(64), primary_key=True, nullable=False, unique=True)
    expires = Column(DateTime, nullable=False)

    def __init__(self, userid, validator, expires):
        self.userid = userid
        self.validator = validator
        self.expires = expires
