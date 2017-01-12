import unittest
import sys
import time
import re
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *

class FlaskTestCase(unittest.TestCase):

    client = Client('id','secret','Test Client',1,False,'authorized http://127.0.0.1:5000/authorized','A S T P N')
    user = Users(1, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
    address = Addresses(1, '123 Main St', '#101', 'Detroit', 'MI', '48226')
    school = Schools(1, 'Detroit High', 1, 1)
    code = Codes('123456', datetime.utcnow() + timedelta(days=30), 1)
    token = Token(0,'id',1,'Bearer','acc','ref',datetime.utcnow() + timedelta(days=30),'A S T P N')

    def setUp(self):
        self.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))
        time.sleep(.1)

        if db.session.query(Users).get(1) is None:
            db.session.add(self.client)
            db.session.add(self.user)
            db.session.add(self.address)
            db.session.add(self.school)
            db.session.add(self.code)
            db.session.add(self.token)
            db.session.commit()


    def tearDown(self):
        Base.metadata.drop_all(db.get_engine(app))


    def test_unauthorized(self):
        rv = self.app.get('/user/{0}'.format(self.user.id))
        self.assertIn('Unauthorized', str(rv.data))

    '''
    Get authorization code from grant.
    Code will be used later to get token using authorization_code grant type.
    '''
    def test_oauth_authorize(self):
        client = 'client_id='+self.client.client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'

        rv = self.app.post('/oauth/authorize?{0}&{1}&{2}&{3}'.format(client,redirect_uri, scope, response),
                           data=dict(code=self.code.six_digits, userid=self.user.id))

        self.assertNotIn('error', rv.location)
        self.assertIn('code', str(rv.location))

    '''
    Get access_token, refresh_token, expires_in...
    Use authorization_code grant type.
    '''
    def test_oauth_token_authorization_code(self):
        db.session.add(self.code)
        client = 'client_id='+self.client.client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'
        grant_type = 'grant_type=authorization_code'

        rv_auth = self.app.post('/oauth/authorize?{0}&{1}&{2}&{3}'.format(client,redirect_uri, scope, response),
                           data=dict(code=self.code.six_digits, userid=self.user.id))
        auth_code = rv_auth.location.split('=')[-1]

        rv = self.app.post('/oauth/token?{0}&{1}&code={2}&{3}&{4}'.format(grant_type,client,auth_code,scope,redirect_uri))
        # rv_token = re.split(':|,',str(rv.data))
        # pprint.pprint(rv_token)

        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))


    def test_authorized(self):
        rv = self.app.get('/user/1?access_token={0}'.format(self.token.access_token))
        self.assertNotIn('Unauthorized', str(rv.data))

    def test_update_user_password(self):
        rv = self.app.post('/update/1?access_token={0}'.format(self.token.access_token),
                           data=dict(password='password!',username='JohnnyD'))
        self.assertIn('password', str(rv.data))
        self.assertIn('username', str(rv.data))

    def test_oauth_token_password(self):
        usernm = 'JohnnyD'
        passwd = 'password!'
        rv_update = self.app.post('/update/1?access_token={0}'.format(self.token.access_token),
                           data=dict(password=passwd, username=usernm))
        client = 'client_id=' + self.client.client_id
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

    def test_oauth_token_refresh(self):
        client = 'client_id=id'
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        grant_type = 'grant_type=refresh_token'
        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&refresh_token={4}'.format(grant_type, client, scope,
                                                                            redirect_uri, self.token.refresh_token))
        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))

    def test_get_user(self):
        rv = self.app.get('/user/1?access_token={0}'.format(self.token.access_token))

        # rv_user = re.split(':|,', str(rv.data))
        # pprint.pprint(rv_user)

        self.assertIn('"addressid": 1', str(rv.data))
        self.assertIn('"email": "jdoe@domain.com"', str(rv.data))
        self.assertIn('"first": "John"', str(rv.data))
        self.assertIn('"id": 1', str(rv.data))
        self.assertIn('"last": "Doe"', str(rv.data))
        self.assertIn('"role": "S"', str(rv.data))
        self.assertIn('"schoolid": 1', str(rv.data))
        self.assertIn('"username": "jdoe"', str(rv.data))

    def test_update_user_first_name(self):
        rv = self.app.post('/update/1?access_token={0}'.format(self.token.access_token),
                           data=dict(first='John'))
        self.assertIn('updated', str(rv.data))
        self.assertIn('first', str(rv.data))
        # assert b'updated' in rv.data


if __name__ == '__main__':
    unittest.main()