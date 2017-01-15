import unittest
import sys
# import time
# import re
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *

client_id = 'id'
user_id = 1
six_digits = '123456'
access_token = 'acc'
refresh_token = 'ref'

class FlaskUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))

        CLIENT = Client(client_id, 'secret', 'Test Client', 1, False,
                        HOME_URL + 'authorized http://127.0.0.1:5000/authorized', 'A S T P N')
        USER = Users(user_id, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
        ADDRESS = Addresses(1, '123 Main St', '#101', 'Detroit', 'MI', '48226')
        SCHOOL = Schools(1, 'Detroit High', 1, 1)
        CODE = Codes(six_digits, datetime.utcnow() + timedelta(days=30), 1)
        TOKEN = Token(0,'id',1,'Bearer',access_token,refresh_token,datetime.utcnow() + timedelta(days=30),'A S T P N')

        if db.session.query(Users).get(1) is None:
            print('Added to DB')
            db.session.add(CLIENT)
            db.session.add(USER)
            db.session.add(ADDRESS)
            db.session.add(SCHOOL)
            db.session.add(CODE)
            db.session.add(TOKEN)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        print('Deleted from DB')
        Base.metadata.drop_all(db.get_engine(app))
        pass

    def resetToken(self):
        tok = db.session.query(Token).filter_by(user=1).first()
        tok.access_token = access_token
        tok.refresh_token = refresh_token
        db.session.commit()

    def addCode(self):
        CODE = Codes(six_digits, datetime.utcnow() + timedelta(days=30), 1)
        db.session.add(CODE)
        db.session.commit()


class FlaskUserUnitTest(FlaskUnitTest):

    @classmethod
    def setUpClass(cls):
        super(FlaskUserUnitTest, cls).setUpClass()
        print('starting User Tests')

    def test_get_user(self):
        access = 'access_token=' + access_token
        rv = self.app.get('/user/1?{0}'.format(access))
        # rv_split = re.split(':|,', str(rv.data))
        # pprint.pprint(rv_split)

        self.assertIn('"addressid": 1', str(rv.data))
        self.assertIn('"email": "jdoe@domain.com"', str(rv.data))
        self.assertIn('"first": "John"', str(rv.data))
        self.assertIn('"id": 1', str(rv.data))
        self.assertIn('"last": "Doe"', str(rv.data))
        self.assertIn('"role": "S"', str(rv.data))
        self.assertIn('"schoolid": 1', str(rv.data))
        self.assertIn('"username": "jdoe"', str(rv.data))

    def test_update_user_first_name(self):
        access = 'access_token='+access_token
        rv = self.app.post('/update/1?{0}'.format(access),
                           data=dict(first='John'))
        self.assertIn('updated', str(rv.data))
        self.assertIn('first', str(rv.data))

class FlaskOauthUnitTest(FlaskUnitTest):

    @classmethod
    def setUpClass(cls):
        super(FlaskOauthUnitTest, cls).setUpClass()
        print('starting OAuth Tests')

    def test_unauthorized(self):
        rv = self.app.get('/user/{0}'.format(user_id))
        self.assertIn('Unauthorized', str(rv.data))

    '''
    Get authorization code from grant.
    Code will be used later to get token using authorization_code grant type.
    '''
    def test_oauth_authorize(self):
        client = 'client_id='+client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'
        rv = self.app.post('/oauth/authorize?{0}&{1}&{2}&{3}'.format(client,redirect_uri, scope, response),
                           data=dict(code=six_digits, userid=user_id))

        self.assertNotIn('error', str(rv.location))
        self.assertIn('code', str(rv.location))

    '''
    Get access_token, refresh_token, expires_in...
    Use authorization_code grant type.
    '''
    def test_oauth_token_authorization_code(self):
        self.addCode()
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'
        grant_type = 'grant_type=authorization_code'
        rv_auth = self.app.post('/oauth/authorize?{0}&{1}&{2}&{3}'.format(client, redirect_uri, scope, response),
                                data=dict(code=six_digits, userid=user_id))
        self.failIf('Error' in str(rv_auth.data))
        auth_code = 'code=' + str(rv_auth.location).split('=')[-1]

        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&{4}'.format(grant_type,client,auth_code,scope,redirect_uri))
        # rv_token = re.split(':|,',str(rv.data))
        # pprint.pprint(rv_token)

        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))
        self.resetToken()


    def test_authorized(self):
        access = 'access_token=' + access_token
        rv = self.app.get('/user/1?{0}'.format(access))
        self.assertNotIn('Unauthorized', str(rv.data))

    def test_update_user_password(self):
        access = 'access_token=' + access_token
        rv = self.app.post('/update/1?{0}'.format(access),
                           data=dict(password='password!',username='JohnnyD'))
        self.assertIn('password', str(rv.data))
        self.assertIn('username', str(rv.data))

    def test_oauth_token_password(self):
        usernm = 'JohnnyD'
        passwd = 'password!'
        access = 'access_token=' + access_token
        rv_update = self.app.post('/update/1?{0}'.format(access),
                                  data=dict(password=passwd, username=usernm))
        self.assertIn('updated', str(rv_update.data))
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        grant_type = 'grant_type=password'
        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&username={4}&password={5}'.format(grant_type,client,scope,
                                                                                           redirect_uri,usernm,passwd))
        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))
        self.resetToken()

    def test_oauth_token_refresh(self):
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        grant_type = 'grant_type=refresh_token'
        refresh = 'refresh_token='+ refresh_token
        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&{4}'.format(grant_type, client, scope,
                                                                    redirect_uri, refresh))
        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))
        self.resetToken()

if __name__ == '__main__':
    unittest.main()