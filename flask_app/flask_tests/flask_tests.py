import unittest
import sys
import time
import re
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))

        time.sleep(.1)

        self.__class__.client = Client('id', 'secret', 'Test Client', 1, False,
                                       'http://api.mygameplan.io/authorized http://127.0.0.1:5000/authorized', 'A S T P N')
        self.__class__.user = Users(1, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
        self.__class__.address = Addresses(1, '123 Main St', '#101', 'Detroit', 'MI', '48226')
        self.__class__.school = Schools(1, 'Detroit High', 1, 1)
        self.__class__.code = Codes('123456', datetime.utcnow() + timedelta(days=30), 1)
        self.__class__.token = Token(0,'id',1,'Bearer','acc','ref',datetime.utcnow() + timedelta(days=30),'A S T P N')

        if db.session.query(Users).get(1) is None:
            db.session.add(self.__class__.client)
            db.session.add(self.__class__.user)
            db.session.add(self.__class__.address)
            db.session.add(self.__class__.school)
            db.session.add(self.__class__.code)
            db.session.add(self.__class__.token)
            db.session.commit()


    def tearDown(self):
        pass
        Base.metadata.drop_all(db.get_engine(app))


    def test_unauthorized(self):
        rv = self.app.get('/user/1')
        self.assertIn('Unauthorized', str(rv.data))

    '''
    Get authorization code from grant.
    Code will be used later to get token using authorization_code grant type.
    '''
    def test_oauth_authorize(self):
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'

        rv = self.app.post('/oauth/authorize?client_id={0}&{1}&{2}&{3}'.format(self.__class__.client.client_id,
            redirect_uri, scope, response),data=dict(code=self.__class__.code.six_digits, userid=self.__class__.user.id))

        self.assertNotIn('error', rv.location)
        self.assertIn('code', str(rv.location))

    '''
    Get access_token, refresh_token, expires_in...
    Use authorization_code grant type.
    '''
    def test_oauth_token_authorization_code(self):
        db.session.add(self.__class__.code)
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'
        type = 'grant_type=authorization_code'

        rv_auth = self.app.post('/oauth/authorize?client_id={0}&{1}&{2}&{3}'.format(self.__class__.client.client_id,
                                                                               redirect_uri, scope, response),
                           data=dict(code=self.__class__.code.six_digits, userid=self.__class__.user.id))
        auth_code = rv_auth.location.split('=')[-1]

        rv = self.app.post('/oauth/token?{0}&client_id={1}&code={2}&{3}&{4}'.format(type,self.__class__.client.client_id,
                                                                                    auth_code,scope,redirect_uri))
        # rv_token = re.split(':|,',str(rv.data))
        # pprint.pprint(rv_token)

        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))


    def test_authorized(self):
        rv = self.app.get('/user/1?access_token={0}'.format(self.__class__.token.access_token))
        self.assertNotIn('Unauthorized', str(rv.data))

    def test_get_user(self):
        rv = self.app.get('/user/1?access_token={0}'.format(self.__class__.token.access_token))

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

    def test_update_user(self):
        rv = self.app.post('/update/1?access_token={0}'.format(self.__class__.token.access_token), data=dict(first='John'))
        self.assertIn('updated', str(rv.data))
        self.assertIn('first', str(rv.data))
        # assert b'updated' in rv.data
        # assert b'first' in rv.data

if __name__ == '__main__':
    unittest.main()