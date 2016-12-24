from flask_app import app, db, oauth
from flask_app.models import *
from flask_app.oauth import current_user, randomString
from flask import redirect, request, render_template, session, jsonify
from flask_mail import Mail, Message

mailer = Mail(app)

@app.route('/me')
def me():
    user = current_user()
    return jsonify(username=user.username)


@app.route('/test')
def test():
    # for i in request.environ:
    #     print("{0}:{1}".format(i,request.environ[i]))
    print(request.user_agent.platform, request.user_agent.browser)
    return request.user_agent.platform+" "+request.user_agent.browser


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        args = Users.reqLogin().parse_args(strict=True)
        user = db.session.query(Users).filter_by(username=args['username']).first()
        if not user:
            return "not authenticated"

        session['id'] = user.id
        return redirect('/')
    user = current_user()
    return render_template('login.html', user=user)


@app.route('/user-<int:id>', methods=['GET'])
@oauth.require_oauth()
def getUser(id):
    user = db.session.query(Users).get(id)
    return user.JSON()


@app.route('/add', methods=['POST'])
@oauth.require_oauth()
def postUser():
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


@app.route('/validator-<string:v>', methods=['GET'])
def getValidator(v):
    validator = db.session.query(Validators).filter_by(validator=v).first()
    user = db.session.query(Users).get(validator.userid)
    return user.JSON()
