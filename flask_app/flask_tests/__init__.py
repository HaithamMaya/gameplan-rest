import unittest
import sys
import re
sys.path.insert(0, './flask_app')
from flask_app.__init__ import *
from flask_app.models import *

client_id = 'id'
user_id = 0
six_digits = '123456'
access_token = 'acc'
refresh_token = 'ref'

class FlaskUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        Base.metadata.create_all(db.get_engine(app))
        cls.resetDB()

    @classmethod
    def tearDownClass(cls):
        print('Deleted from DB')
        Base.metadata.drop_all(db.get_engine(app))
        pass

    @classmethod
    def resetDB(cls):
        CLIENT = Client(client_id, 'secret', 'Test Client', user_id, False,
                        HOME_URL + 'authorized http://127.0.0.1:5000/authorized', 'A S T P N')
        USER = Users(user_id, "John", "Doe", "jdoe", "jdoe@domain.com", "S", 0, 0, None, None)
        ADDRESS = Addresses(0, '123 Main St', '#101', 'Detroit', 'MI', '48226')
        SCHOOL = Schools(0, 'Detroit High', 0, 0)
        CODE = Codes(six_digits, datetime.utcnow() + timedelta(days=30), 0)
        TOKEN = Token(0, 'id', user_id, 'Bearer', access_token, refresh_token, datetime.utcnow() + timedelta(days=30),
                      'A S T P N')
        db.session.add(CLIENT)
        db.session.add(USER)
        db.session.add(ADDRESS)
        db.session.add(SCHOOL)
        db.session.add(CODE)
        db.session.add(TOKEN)
        db.session.commit()
        print('Added to DB')

    def resetToken(self):
        tok = db.session.query(Token).filter_by(user=user_id).first()
        tok.access_token = access_token
        tok.refresh_token = refresh_token
        db.session.commit()

    def addCode(self):
        CODE = Codes(six_digits, datetime.utcnow() + timedelta(days=30), user_id)
        db.session.add(CODE)
        db.session.commit()

from flask_tests.flask_oauth_tests import *
from flask_tests.flask_user_tests import *

if __name__ == '__main__':
    unittest.main()