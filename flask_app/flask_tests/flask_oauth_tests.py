from flask_tests.__init__ import *

class FlaskOauthUnitTest(FlaskUnitTest):

    @classmethod
    def setUpClass(cls):
        super(FlaskOauthUnitTest, cls).setUpClass()
        print('Running OAuth Tests')

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
        self.addCode()
        self.assertNotIn('error', str(rv.location))
        self.assertIn('code', str(rv.location))

    '''
    Get access_token, refresh_token, expires_in...
    Use authorization_code grant type.
    '''
    def test_oauth_token_authorization_code(self):
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'
        grant_type = 'grant_type=authorization_code'
        rv_auth = self.app.post('/oauth/authorize?{0}&{1}&{2}&{3}'.format(client, redirect_uri, scope, response),
                                data=dict(code=six_digits, userid=user_id))
        self.addCode()
        self.assertNotIn('Error', str(rv_auth.data))
        auth_code = 'code=' + str(rv_auth.location).split('=')[-1]

        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&{4}'.format(grant_type,client,auth_code,scope,redirect_uri))
        # rv_token = re.split(':|,',str(rv.data))
        # pprint.pprint(rv_token)
        self.resetToken()
        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))

    def test_authorized(self):
        access = 'access_token=' + access_token
        rv = self.app.get('/user/{0}?{1}'.format(user_id, access))
        self.assertNotIn('Unauthorized', str(rv.data))

    def test_update_user_password(self):
        access = 'access_token=' + access_token
        rv = self.app.post('/update/{0}?{1}'.format(user_id, access),
                           data=dict(password='password!',username='JohnnyD'))
        self.assertIn('password', str(rv.data))
        self.assertIn('username', str(rv.data))

    def test_oauth_token_password(self):
        usernm = 'JohnnyD'
        passwd = 'password!'
        access = 'access_token=' + access_token
        rv_update = self.app.post('/update/{0}?{1}'.format(user_id, access),
                                  data=dict(password=passwd, username=usernm))
        self.assertIn('updated', str(rv_update.data))
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        grant_type = 'grant_type=password'
        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}&username={4}&password={5}'.format(grant_type,client,scope,
                                                                                           redirect_uri,usernm,passwd))
        self.resetToken()
        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))


    def test_oauth_token_refresh(self):
        client = 'client_id=' + client_id
        redirect_uri = 'redirect_uri=http://127.0.0.1:5000/authorized'
        grant_type = 'grant_type=refresh_token'
        refresh = 'refresh_token='+ refresh_token
        rv = self.app.post('/oauth/token?{0}&{1}&{2}&{3}'.format(grant_type, client,
                                                                    redirect_uri, refresh))
        self.resetToken()
        self.assertNotIn('error', str(rv.data))
        self.assertNotIn('Token.scopes', str(rv.data))
        print(str(rv.data))

        self.assertIn('access_token', str(rv.data))
        self.assertIn('scope', str(rv.data))
        self.assertIn('expires_in', str(rv.data))
        self.assertIn('token_type', str(rv.data))
        self.assertIn('refresh_token', str(rv.data))
