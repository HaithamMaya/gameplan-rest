from flask_app import app, db, oauth
from flask_app.models import Users, Validators
from flask_app.oauth2 import current_user, randomString
from flask import redirect, request, render_template, session, jsonify
from flask_mail import Mail, Message

mailer = Mail(app)

@app.route('/test')
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
    requests = []
    for i in request.environ:
        requests.append("{0}: {1}".format(i,request.environ[i]))
    #print(request.user_agent.platform, request.user_agent.browser)
    return jsonify(requests)


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
    user = Users(None,args['first'],args['last'],None,args['email'],args['role'],args['schoolid'],
                 args['addressid'],None,None)
    db.session.add(user)
    db.session.commit()
    validator = Validators(user.id, randomString(), None)
    db.session.add(validator)
    db.session.commit()

    msg = Message("Welcome to Gameplan")
    msg.add_recipient(user.email)
    msg.html = render_template('alert.html', first=user.first, last=user.last,
                               school='Some Random High School', validator=validator.validator)
    mailer.send(msg)
    print('sent {0}'.format(user.id))
    return user.JSON()


@app.route('/validator/<string:v>', methods=['GET'])
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
    validator = db.session.query(Validators).filter_by(validator=v).first()
    user = db.session.query(Users).get(validator.userid)
    return user.JSON()