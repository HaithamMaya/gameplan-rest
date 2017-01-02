# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Addres(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    line1 = Column(String(100), nullable=False)
    line2 = Column(String(100))
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)


class Brag(Base):
    __tablename__ = 'brag'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    authorid = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    media = Column(String(64))
    body = Column(String(512))
    categoryid = Column(Integer)
    approverid = Column(Integer)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    type = Column(String(1), nullable=False)


class Client(Base):
    __tablename__ = 'client'

    name = Column(String(40), server_default=text("NULL::character varying"))
    userid = Column(Integer, nullable=False)
    client_id = Column(String(50), primary_key=True, unique=True)
    secret = Column(String(64), nullable=False, unique=True)
    confidential = Column(Boolean, nullable=False, server_default=text("true"))
    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)


class Code(Base):
    __tablename__ = 'code'

    six_digits = Column(String(6), primary_key=True)
    expires = Column(DateTime)
    userid = Column(Integer, nullable=False, unique=True)


class Connection(Base):
    __tablename__ = 'connection'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    userid1 = Column(Integer, nullable=False)
    userid2 = Column(Integer, nullable=False)
    status = Column(String(1))
    actionid = Column(Integer)


class Gameplan(Base):
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

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('grant_id_seq'::regclass)"))
    user = Column(Integer, nullable=False)
    client_id = Column(String(50), nullable=False)
    code = Column(String(255), nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    _scopes = Column(Text)


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('rating_id_seq'::regclass)"))
    gameplanid = Column(Integer, nullable=False)
    score = Column(Float)
    created = Column(DateTime)


class School(Base):
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('school_id_seq'::regclass)"))
    name = Column(String(100), nullable=False)
    adminid = Column(Integer, nullable=False)
    addressid = Column(Integer, nullable=False)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('token_id_seq'::regclass)"))
    client_id = Column(String(50), nullable=False)
    user = Column(Integer)
    token_type = Column(String(40))
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('users_id_seq'::regclass)"))
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


class Validator(Base):
    __tablename__ = 'validator'

    userid = Column(Integer, nullable=False)
    validator = Column(String(256), primary_key=True, unique=True)
    expires = Column(DateTime, nullable=False)
