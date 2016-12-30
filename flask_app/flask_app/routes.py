from flask_app.__init__ import app, db, oauth, HOME_URL, ENCRYPTION_METHOD
from flask_app.models import Users, Validators, Codes, Schools
from flask_app.oauth2 import randomString
from flask import redirect, request, render_template, session, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import urllib.parse as parse
import pprint

mailer = Mail(app)
VALIDATOR_DURATION_DAYS = 30
CODE_DURATION_MINUTES = 15


@app.route('/test', methods=['GET', 'POST'])
def test():
    """
    Test function
    Returns random stuff
    ---
    tags:
      - Test
    parameters:
      - name: something
        in: path
        type: string
        required: false
    responses:
      '200':
        description: Something
        schema:
          id: user_response
          properties:
            something:
              type: string
              description: The **** ?
              default: some_thing
      '401':
        description: Unauthorized
    """
    r = {}
    for i in request.environ:
        r[str(i)] = str(request.environ[i])

    print(app.config['SECRET_KEY'])

    return jsonify(r)


@app.route('/', methods=('GET', 'POST'))
def home():
    return redirect('/apidocs/index.html')


@app.route('/user/<int:id>', methods=['GET'])
@oauth.require_oauth()
def getUser(id):
    """
    Get user
    Returns user object
    ---
    tags:
      - Users
    parameters:
      - name: id
        description: user id
        in: path
        type: integer
        required: true
      - name: access_token
        description: oauth access token
        in: query
        type: string
        required: true
    responses:
      '200':
        description: Returns User information
        schema:
          properties:
            id:
              type: integer
              description: user id
            first:
              type: string
              description: first name
            last:
              type: string
              description: last name
            username:
              type: string
              description: username
            email:
              type: string
              description: email address
            role:
              type: string
              description: user role (scope)
            schoolid:
              type: integer
              description: school id
            addressid:
              type: integer
              description: address id
            created:
              type: string
              format: date-time
              description: time user added to database and sent welcome email
            joined:
              type: string
              format: date-time
              description: time user created username and password
      '401':
        description: Unauthorized
    """
    user = db.session.query(Users).get(id)
    return user.JSON()


@app.route('/add', methods=['POST'])
@oauth.require_oauth()
def postUser():
    """
    Add user
    Adds a new user to the db and sends them a welcome email, then returns added user object
    ---
    tags:
      - Users
    parameters:
      - name: user
        description: user object
        in: body
        schema:
          id: PostUser
          properties:
            first:
              type: string
              description: first name
            last:
              type: string
              description: last name
            email:
              type: string
              description: email address
            role:
              type: string
              description: user role (scope)
            schoolid:
              type: integer
              description: school id
            addressid:
              type: integer
              description: address id
      - name: access_token
        description: oauth access token
        in: query
        type: string
        required: true
    responses:
      '200':
        description: Returns User information
        schema:
          id: GetUser
          properties:
            id:
              type: integer
              description: user id
            first:
              type: string
              description: first name
            last:
              type: string
              description: last name
            username:
              type: string
              description: username
            email:
              type: string
              description: email address
            role:
              type: string
              description: user role (scope)
            schoolid:
              type: integer
              description: school id
            addressid:
              type: integer
              description: address id
            created:
              type: string
              format: date-time
              description: time user added to database and sent welcome email
            joined:
              type: string
              format: date-time
              description: time user created username and password
      '401':
        description: Unauthorized
    """
    args = Users.req().parse_args(strict=True)
    user = Users(None, args['first'], args['last'], None, args['email'], args['role'], args['schoolid'],
                 args['addressid'], None, None)
    db.session.add(user)
    db.session.commit()
    school = db.session.query(Schools).get(user.schoolid)
    expires = datetime.utcnow() + timedelta(days=VALIDATOR_DURATION_DAYS)
    validator = Validators(user.id, randomString(), expires)
    db.session.add(validator)
    db.session.commit()
    email = user.email.split('@')[0]
    url = HOME_URL + 'validate/' + validator.validator + '?email=' + parse.quote(email, safe='')

    msg = Message("Welcome to Gameplan")
    msg.add_recipient(user.email)
    msg.html = render_template('welcome.html', first=user.first, last=user.last,
                               school=school.name, url=url)
    mailer.send(msg)
    print('sent {0}'.format(url))
    return user.JSON()


@app.route('/update/<int:id>', methods=['POST'])
@oauth.require_oauth()
def updateUser(id):
    """
    Update user
    Updates specified fields then returns updated user object
    ---
    tags:
      - Users
    parameters:
      - id: user id
        description: user object
        in: body
        schema:
          id: PostUser
          properties:
            first:
              type: string
              description: first name
            last:
              type: string
              description: last name
            email:
              type: string
              description: email address
            role:
              type: string
              description: user role (scope)
            schoolid:
              type: integer
              description: school id
            addressid:
              type: integer
              description: address id
      - name: access_token
        description: oauth access token
        in: query
        type: string
        required: true
    responses:
      '200':
        description: Returns User information
        schema:
          id: GetUser
          properties:
            updated:
              type: string
              description: fields updated
            id:
              type: integer
              description: user id
            first:
              type: string
              description: first name
            last:
              type: string
              description: last name
            username:
              type: string
              description: username
            email:
              type: string
              description: email address
            role:
              type: string
              description: user role (scope)
            schoolid:
              type: integer
              description: school id
            addressid:
              type: integer
              description: address id
            created:
              type: string
              format: date-time
              description: time user added to database and sent welcome email
            joined:
              type: string
              format: date-time
              description: time user created username and password
      '401':
        description: Unauthorized
    """
    r = []
    user = db.session.query(Users).get(id)
    if user is None:
        return jsonify(Error='Invalid user ID')
    if request.form.get('password') is not None:
        password = request.form.get('password')
        h = generate_password_hash(password + user.role, ENCRYPTION_METHOD, 8).split('$')
        user.salt = h[1]
        user.hash = h[2]
        r.append('password')
    if request.form.get('first') is not None:
        user.first = request.form.get('first')
        r.append('first')
    if request.form.get('last') is not None:
        user.first = request.form.get('last')
        r.append('last')

    db.session.commit()
    return jsonify(updated=r)


@app.route('/validate/<string:v>', methods=['GET', 'POST'])
def getValidator(v):
    """
    Get user from validator
    Gets user info associated with randomly generated validator string
    ---
    tags:
      - Users
    parameters:
      - name: validator
        description: validator string
        in: path
        type: string
        required: true
      - name: email
        description: user email .split('@')[0]
        in: path
        type: string
        required: true
    responses:
      '200':
        description: Returns User ID
        schema:
          id: UserValidated
          properties:
            user:
              type: integer
              description: user id
      '401':
        description: Unauthorized
    """
    if request.args.get('email') is None:
        return jsonify({'Error': 'Invalid!'})
    validator = validatorInvalid(v, parse.unquote(request.args.get('email')))
    if type(validator) is not Validators:
        return jsonify(validator)
    elif request.method == 'POST':
        return sendCode(validator, request.args.get('email'))
    else:
        return jsonify({'user': (validator.userid)})


def sendCode(v, email):
    user = db.session.query(Users).get(v.userid)
    expires = datetime.utcnow() + timedelta(minutes=CODE_DURATION_MINUTES)
    code = Codes(randomString(6, '1234567890'), expires, v.userid)
    db.session.add(code)
    url = HOME_URL + '/validate/' + v.validator + '?email=' + email

    msg = Message("Verification Code")
    msg.add_recipient(user.email)
    msg.html = render_template('verify.html', first=user.first, code=code.six_digits, url=url)
    mailer.send(msg)
    print('sent {0} {1}'.format(user.id, user.email))
    return jsonify({'Sent': user.email, 'Expires': expires})


def validatorInvalid(v, email):
    validator = db.session.query(Validators).filter_by(validator=v).first()
    if validator is None:
        return {'Error': 'Validator not found'}
    user = db.session.query(Users).get(validator.userid)
    if email != user.email.split('@')[0]:
        return {'Error': 'Invalid email'}
    elif validator.expires < datetime.utcnow():
        return {'Error': 'Expired'}
    else:
        return validator
