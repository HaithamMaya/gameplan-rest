import sys
sys.path.insert(0, './flask_app')
import os
from flask_app.__init__ import *
from sqlalchemy.engine import create_engine
from flask_app.models import Base
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        self.token = 'access_token=JM0VKiGtHifM4oeNLeuUvuzDwOwNYy'
        engine = create_engine('postgresql://localhost')
        Base.metadata.create_all(engine)

        # user = Users(None, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
        # db.session.add(user)
        # db.session.commit()

        # with flaskapp.app.app_context():
        #     flaskapp.init_db()

    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(app.config['DATABASE'])
        print('End')

    # def test_unauthorized(self):
    #     rv = self.app.get('/user/1')
    #     assert b'Unauthorized' in rv.data

    # def test_authorized(self):
    #     rv = self.app.get('/user/1?{0}'.format(self.token))
    #     assert not b'Unauthorized' in rv.data

    def test_get_user(self):
        rv = self.app.get('/user/1?{0}'.format(self.token))
        assert b'"addressid": 1' in rv.data
        # assert b'"created": "Sun, 06 Nov 2016 09:30:53 GMT"' in rv.data
        assert b'"email": "jdoe@domain.com"' in rv.data
        assert b'"first": "John"' in rv.data
        assert b'"id": 1' in rv.data
        #assert b'"joined": null' in rv.data
        assert b'"last": "Doe"' in rv.data
        assert b'"role": "S"' in rv.data
        assert b'"schoolid": 1' in rv.data
        assert b'"username": "jdoe"' in rv.data

    # def test_update_user(self):
    #     rv = self.app.post('/update/1?{0}'.format(self.token), data=dict(first='John'))
    #     assert b'updated' in rv.data
    #     assert b'first' in rv.data

if __name__ == '__main__':
    unittest.main()