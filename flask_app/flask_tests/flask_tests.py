import sys
import time
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *
from flask import g
import unittest

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))

        time.sleep(.1)

        self.__class__.client = Client('id', 'secret', 'Test Client', 1, False,
                                       'http://api.mygameplan.io/authorized http://127.0.0.1:5000/authorized', 'A S T P N')
        self.__class__.user = Users(1, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 1, 1, None, None)
        self.__class__.address = Addresses(None, '123 Main St', '#101', 'Detroit', 'MI', '48226')
        self.__class__.school = Schools(None, 'Detroit High', 1, 1)
        self.__class__.code = Codes('123456', datetime.utcnow() + timedelta(days=30), 1)

        if db.session.query(Users).get(1) is None:
            db.session.add(self.__class__.client)
            db.session.add(self.__class__.user)
            db.session.add(self.__class__.address)
            db.session.add(self.__class__.school)
            db.session.add(self.__class__.code)
            db.session.commit()


    def tearDown(self):
        pass
        #Base.metadata.drop_all(db.get_engine(app))


    def test_unauthorized(self):
        rv = self.app.get('/user/1')
        assert b'Unauthorized' in rv.data

    def test_oauth_authorize(self):
        redirect = 'redirect_uri=http://127.0.0.1:5000/authorized'
        scope = 'scope=A'
        response = 'response_type=code'

        rv = self.app.post('/oauth/authorize?client_id={0}&{1}&{2}&{3}'.format(self.__class__.client.client_id, redirect, scope, response),
                           data=dict(code=self.__class__.code.six_digits, userid=self.__class__.user.id))

        self.assertNotIn('error', rv.location)
        self.assertIn('code', rv.location)


    # def test_oauth_authorizeeee(self):
    #     rv_add = self.app.post('/add'.format(), data=dict(first='Jane',last='Doe',email='janed@domain.com',
    #                                              role='S',schoolid=1,addressid=1))
    #     pprint.pprint(rv_add)
    #     code = db.session.query(Codes).filter_by(userid=2).first()
    #     rv = self.app.post('/oauth/authorize'.format(self.client.id,),
    #                        data=dict(code=code.six_digits, userid=rv_add['id']))

    # def test_authorized(self):
    #
    #
    #     rv = self.app.get('/user/1?{0}'.format(self.token))
    #     assert not b'Unauthorized' in rv.data

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