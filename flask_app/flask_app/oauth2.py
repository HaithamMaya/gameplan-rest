from flask_app.__init__ import app, db, oauth, HOME_URL
from flask_app.models import Client, Grant, Token, Users, Codes
from flask import redirect, request, render_template, session, jsonify
from werkzeug.security import gen_salt
from datetime import datetime, timedelta
import random
import string
from hashlib import sha512
import pprint

SIMPLE_CHARS = string.ascii_letters + string.digits

@app.route('/client', methods=['POST'])
def client():
    """
    New client
    Adds a new client and returns id and secret
    ---
    tags:
      - OAuth
    parameters:
      - name: verification
        description: verification code and user id
        in: body
        schema:
          id: Verify
          properties:
            code:
              type: string
              description: six-digit code
            userid:
              type: integer
              description: user id
    responses:
      '200':
        description: Client
        schema:
          id: Client
          properties:
            client_id:
              type: string
              description: client id
            client_secret:
              type: string
              description: client secret
      '401':
        description: Unauthorized
    """
    args = Codes.req().parse_args(strict=True)
    six_digits = args.get('code')
    if six_digits is None:
        return jsonify(Error='No Code')
    userid = args.get('userid')
    code = checkCode(six_digits, userid)
    if type(code) is not Codes:
        return jsonify(code)

    user = db.session.query(Users).get(userid)
    if request.user_agent.platform:
        client_name = request.user_agent.platform + " " + request.user_agent.browser
    else:
        client_name = 'NONE'
    item = Client(gen_salt(40), gen_salt(50), client_name, userid, False,
                  ' '.join([
                      HOME_URL+'/authorized',
                      'http://127.0.0.1:5000/authorized',
                  ]), user.role
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(
        client_id=item.client_id,
        client_secret=item.secret,
    )

@app.route('/oauth/authorize', methods=['POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    """
    Authorize client
    Adds a grant for the current user and client in session
    ---
    tags:
      - OAuth
    parameters:
      - name: client_id
        in: query
        type: string
        required: true
      - name: redirect_uri
        in: query
        type: string
        required: true
      - name: scope
        in: query
        type: string
        required: true
      - name: response_type
        in: query
        type: string
        required: true
    responses:
      '200':
        description: Redirects to /authorized
      '401':
        description: Unauthorized
    """
    return True

@app.route('/authorized', methods=['GET'])
def authorized():
    """
        Client authorized
        redirect page after client receives grant
        ---
        tags:
          - OAuth
        responses:
          '200':
            description: Code (or error)
            schema:
              id: Response code
              properties:
                code:
                  type: string
                  description: grant code
          '401':
            description: Unauthorized
        """
    return jsonify(request.values)

@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    """
        Token generator
        Takes 4 different payloads dependent on which grant_type specified
        ---
        tags:
          - OAuth
        parameters:
          - name: grant_type
            description: password, client_credentials, refresh_token, authorization_code
            in: query
            type: string
            required: true
            default:
          - name: client_id
            description: client id
            in: query
            type: string
            required: true
          - name: scope
            description: client id
            in: query
            type: string
            required: true
          - name: redirect_uri
            description: redirect uri
            in: query
            type: string
            required: true
            default: http://127.0.0.1:5000/authorized
          - name: refresh_token
            description: refresh token
            in: query
            type: string
            required: false
          - name: code
            description: authorization code from grant
            in: query
            type: string
            required: false
          - name: client_secret
            description: client secret
            in: query
            type: string
            required: false
          - name: username
            description: username
            in: query
            type: string
            required: false
          - name: password
            description: password
            in: query
            type: string
            format: password
            required: false
        responses:
          '200':
            description: Returns Token
            schema:
              id: Token
              properties:
                access_token:
                  type: string
                  description: access token
                refresh_token:
                  type: string
                  description: refresh token
                scope:
                  type: string
                  description: scope (user role)
                token_type:
                  type: string
                  description: only bearer tokens supported
                  default: Bearer
                expires_in:
                  type: integer
                  description: time in seconds until access token expires
          '401':
            description: Unauthorized
        """
    return None

@app.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass


@oauth.clientgetter
def load_client(id):
    return db.session.query(Client).get(id)


@oauth.grantgetter
def load_grant(client_id, code):
    return db.session.query(Grant).filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(None, current_user().id, client_id, code['code'], request.redirect_uri, expires, ' '.join(request.scopes))
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return db.session.query(Token).filter_by(access_token=access_token).first()
    elif refresh_token:
        return db.session.query(Token).filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = db.session.query(Token).filter_by(client_id=request.client.client_id,
                                 user=request.user)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)
    expiresin = token['expires_in']
    expires = datetime.utcnow() + timedelta(seconds=expiresin)

    tok = Token(None, request.client.client_id, request.user, token['token_type'], token['access_token'],
                token['refresh_token'], expires, token['scope'])
    db.session.add(tok)
    db.session.commit()
    return tok

@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = db.session.query(Users).filter_by(username=username).first()
    #if user.check_password(password):
        #return user
    return user

def current_user():
    if 'id' in session:
        uid = session['id']
        return db.session.query(Users).get(uid)
    return None

def randomString(choices=SIMPLE_CHARS, length=64):
    return ''.join(random.choice(choices) for i in range(length))

def randomHash(length=32):
    hash = sha512()
    hash.update(randomString())
    return hash.hexdigest()[:length]

def checkCode(c, userid):
    code = db.session.query(Codes).get(c)
    if code is None:
        return {'Error':'Code not found'}
    elif datetime.utcnow() > code.expires:
        return {'Error':'Expired'}
    elif str(code.userid) != userid:
        print(code.userid, ' != ',userid)
        return {'Error': 'User ID does not match'}
    else:
        return code
