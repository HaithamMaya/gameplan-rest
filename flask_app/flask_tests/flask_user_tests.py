from flask_tests.__init__ import *

class FlaskUserUnitTest(FlaskUnitTest):

    @classmethod
    def setUpClass(cls):
        super(FlaskUserUnitTest, cls).setUpClass()
        print('Running User Tests')

    def test_get_user(self):
        access = 'access_token=' + access_token
        rv = self.app.get('/user/{0}?{1}'.format(user_id, access))
        # rv_split = re.split(':|,', str(rv.data))
        # pprint.pprint(rv_split)

        self.assertIn('"addressid": 0', str(rv.data))
        self.assertIn('"email": "jdoe@domain.com"', str(rv.data))
        self.assertIn('"first": "John"', str(rv.data))
        self.assertIn('"id": 0', str(rv.data))
        self.assertIn('"last": "Doe"', str(rv.data))
        self.assertIn('"role": "S"', str(rv.data))
        self.assertIn('"schoolid": 0', str(rv.data))
        self.assertIn('"username": "jdoe"', str(rv.data))

    def test_update_user_first_name(self):
        access = 'access_token='+access_token
        rv = self.app.post('/update/{0}?{1}'.format(user_id, access),
                           data=dict(first='John'))
        self.assertIn('updated', str(rv.data))
        self.assertIn('first', str(rv.data))

    def test_add_user(self):
        access = 'access_token=' + access_token
        rv = self.app.post('/add?{0}'.format(access),
                           data=dict(first='Billy',last='Roberts',email='brobby@domain.com',role='S',schoolid=0))
        self.assertIn('"addressid": null', str(rv.data))
        self.assertIn('"email": "brobby@domain.com"', str(rv.data))
        self.assertIn('"first": "Billy"', str(rv.data))
        self.assertIn('"id": 1', str(rv.data))
        self.assertIn('"last": "Roberts"', str(rv.data))
        self.assertIn('"role": "S"', str(rv.data))
        self.assertIn('"schoolid": 0', str(rv.data))

    def test_get_validate_user(self):
        access = 'access_token=' + access_token
        v = db.session.query(Validators).filter((Validators.userid > 0)).first()
        if(type(v) != Validators):
            rv_add = self.app.post('/add?{0}'.format(access),
                           data=dict(first='Billy', last='Roberts', email='brobby@domain.com', role='S',schoolid=0))
            v = db.session.query(Validators).filter((Validators.userid > 0)).first()

        u = db.session.query(Users).get(v.userid)
        rv = self.app.get('/validate/{0}?email={1}'.format(v.validator,u.email.split('@')[0]))
        self.assertIn('"email": "{0}"'.format('br*******@d******.***'), str(rv.data))


    def test_post_code_validate_user(self):
        access = 'access_token=' + access_token
        v = db.session.query(Validators).filter((Validators.userid > 0)).first()
        if(type(v) != Validators):
            rv_add = self.app.post('/add?{0}'.format(access),
                           data=dict(first='Billy', last='Roberts', email='brobby@domain.com', role='S',schoolid=0))
            v = db.session.query(Validators).filter((Validators.userid > 0)).first()

        u = db.session.query(Users).get(v.userid)
        rv = self.app.post('/validate/{0}?email={1}'.format(v.validator,u.email.split('@')[0]))

        rv_split = re.split('"Expires"', str(rv.data))
        expires = datetime.strptime(rv_split[-1][3:-7], '%a, %d %b %Y %H:%M:%S %Z')
        self.assertIn('"Email": "{0}"'.format(u.email), str(rv.data))
        self.assertAlmostEqual(expires.strftime('%a, %d %b %Y %H:%M %Z'), (datetime.utcnow()+timedelta(minutes=15)).strftime('%a, %d %b %Y %H:%M %Z'))
