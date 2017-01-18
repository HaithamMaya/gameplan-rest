from flask_tests.__init__ import *

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