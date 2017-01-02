import os
import flask_app.__init__ as flaskapp
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskapp.app.config['DATABASE'] = tempfile.mkstemp()
        flaskapp.app.config['TESTING'] = True
        self.app = flaskapp.app.test_client()
        self.token = 'JM0VKiGtHifM4oeNLeuUvuzDwOwNYy'

        # with flaskapp.app.app_context():
        #     flaskapp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskapp.app.config['DATABASE'])

    def test_unauthorized(self):
        rv = self.app.get('/user/1')
        assert b'Unauthorized' in rv.data

    def test_authorized(self):
        rv = self.app.get('/user/1?access_token={0}'.format(self.token))
        assert not b'Unauthorized' in rv.data

if __name__ == '__main__':
    unittest.main()