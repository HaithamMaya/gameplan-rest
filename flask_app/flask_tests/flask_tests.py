import sys
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *
import unittest

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))

        if db.session.query(Client).get(1) is None:
            self.client = Client('abc123', 'secret', 'Test Client', 1, False, 'http://api.mygameplan.io/authorized', 'A S T P N')
            db.session.add(self.client)
            self.user = Users(None, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
            db.session.add(self.user)
            self.address = Addresses(None, '123 Main St', '#101', 'Detroit', 'MI', '48226')
            db.session.add(self.address)
            self.school = Schools(None, 'Detroit High', 1, 1)
            db.session.add(self.school)
            db.session.commit()


    def tearDown(self):
        pass

    def test_unauthorized(self):
        rv = self.app.get('/user/1')
        assert b'Unauthorized' in rv.data

    def test_authorized(self):

        rv = self.app.get('/user/1?{0}'.format(self.token))
        assert not b'Unauthorized' in rv.data

    # def test_get_user(self):
    #     rv = self.app.get('/user/1?{0}'.format(self.token))
    #     assert b'"addressid": 1' in rv.data
    #     # assert b'"created": "Sun, 06 Nov 2016 09:30:53 GMT"' in rv.data
    #     assert b'"email": "jdoe@domain.com"' in rv.data
    #     assert b'"first": "John"' in rv.data
    #     assert b'"id": 1' in rv.data
    #     #assert b'"joined": null' in rv.data
    #     assert b'"last": "Doe"' in rv.data
    #     assert b'"role": "S"' in rv.data
    #     assert b'"schoolid": 1' in rv.data
    #     assert b'"username": "jdoe"' in rv.data

    # def test_update_user(self):
    #     rv = self.app.post('/update/1?{0}'.format(self.token), data=dict(first='John'))
    #     assert b'updated' in rv.data
    #     assert b'first' in rv.data

if __name__ == '__main__':
    unittest.main()