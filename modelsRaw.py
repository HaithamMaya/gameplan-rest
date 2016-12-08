# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Addres(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('address_id_seq'::regclass)"))
    line1 = Column(String(100), nullable=False)
    line2 = Column(String(100))
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)


class Brag(Base):
    __tablename__ = 'brag'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('brag_id_seq'::regclass)"))
    authorid = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    media = Column(String(64))
    body = Column(String(512))
    categoryid = Column(Integer)
    approverid = Column(Integer)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('category_id_seq'::regclass)"))
    name = Column(String(64), nullable=False)
    type = Column(String(1), nullable=False)


class Client(Base):
    __tablename__ = 'client'

    name = Column(String(40), server_default=text("NULL::character varying"))
    userid = Column(Integer, nullable=False)
    id = Column(String(50), primary_key=True, unique=True)
    secret = Column(String(64), nullable=False, unique=True)
    confidential = Column(Boolean, nullable=False, server_default=text("true"))
    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)


class Connection(Base):
    __tablename__ = 'connection'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('connection_id_seq'::regclass)"))
    userid1 = Column(Integer, nullable=False)
    userid2 = Column(Integer, nullable=False)
    status = Column(String(1))
    actionid = Column(Integer)


class Gameplan(Base):
    __tablename__ = 'gameplan'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('gameplan_id_seq'::regclass)"))
    userid = Column(Integer, nullable=False)
    categoryid = Column(Integer, nullable=False)
    body = Column(String(512), nullable=False)
    status = Column(String(1))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime)


class Grant(Base):
    __tablename__ = 'grant'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('grant_id_seq'::regclass)"))
    userid = Column(Integer, nullable=False)
    clientid = Column(String(50), nullable=False)
    code = Column(String(255), nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    scopes = Column(Text)


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
    clientid = Column(String(50), nullable=False)
    userid = Column(Integer)
    token_type = Column(String(40))
    accesstoken = Column(String(255), unique=True)
    refreshtoken = Column(String(255), unique=True)
    expires = Column(DateTime)
    scopes = Column(Text)


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

    id = Column(Integer, primary_key=True, unique=True)
    validator = Column(String(32), nullable=False, unique=True, server_default=text("now()"))
    date = Column(DateTime, nullable=False, server_default=text("now()"))
