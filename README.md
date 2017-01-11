# gameplan-rest   [![Build Status](https://travis-ci.com/hmaya1/gameplan-rest.svg?token=tzVy2xkvpXAr6ksz4g41&branch=master)](https://travis-ci.com/hmaya1/gameplan-rest)    
http://api.mygameplan.io/   
or  
http://127.0.0.1:5000/  (local)  

###New User Flow
1. User added via POST to `/add`
    * Added user receives email
    * Unique link in email like `/validate/h2349dfnAFh23nn&email=jdoe`
2. User clicks link in email and is prompted to send a code to their email `email=jdoe` to verify their email address
    * GET request returns `"userid": 1`
3. User clicks some sort of "Send Code" button and a POST is sent to `/validate/h2349dfnAFh23nn&email=jdoe`
    * After "Senc Code" pressed, an input appears prompting user to check email
    * User is emailed a 6-digit code `348023`
    * Code is only valid for 30 mins (can be changed to +/-)
4. User copies and pastes code into input (in <30 mins) and a POST is sent to `/oauth/authorize?client_id=<CLIENT>&redirect_uri=<REDIRECT>&scope=N&response_type=code` 
(where the scope N means it's a new user who hasn't created a username or password) with
`{
  "code": "348023",
  "userid": 1
}` in the body
    * A Grant authorization_code is returned like `K75DuasGha3s3`.
    * POST to `oauth/token?grant_type=authorization_code&client_id=<CLIENT>&scope=N&redirect_uri=<REDIRECT>&code=K75DuasGha3s3` returns 
`{
  "token_type": "Bearer",
  "expires_in": 86400,
  "access_token": "I2xe2Ph1rHSdFqHrNgXYFPkkuNOz35",
  "scope": "N",
  "refresh_token": "eoPUy1XHAh5BuKxEd3rCD8KRW4Uyua"
}`
5. User is redirected to New User page where they can update their username and password
    * `?access_token=I2xe2Ph1rHSdFqHrNgXYFPkkuNOz35` must be in query to all pages where oauth is required


###Example POSTs to OAuth
* `http://127.0.0.1:5000/oauth/authorize?client_id=AtU3ehAtLnpGF88dlbU2PrOXfk4oJdsqL5zR4van&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorized&scope=A&response_type=code`
    * `{
 "code": "348023",
 "userid": 1 }`
 
* `http://127.0.0.1:5000/oauth/token?grant_type=authorization_code&client_id=AtU3ehAtLnpGF88dlbU2PrOXfk4oJdsqL5zR4van&scope=A&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorized&code=K75Dus5wdkfNtqaxqkmcgqMEanS8uZ`





###References for installed packages  
https://pythonhosted.org/Flask-Security/  
http://flask.pocoo.org/docs/0.11/patterns/sqlalchemy/  
https://flask-restplus.readthedocs.io/en/stable/   
https://flask-oauthlib.readthedocs.io/en/latest/oauth2.html#example-for-oauth-2   
https://github.com/rochacbruno/flasgger/blob/master/flasgger/example_app.py   
http://swagger.io/specification/#schemaObject   


###Packages installed
```
pip3 install flask
#pip3 install flask-restplus
pip3 install flask-sqlalchemy
#pip3 install flask-security
pip3 install flask-oauthlib
pip3 install sqlalchemy
pip3 install flasgger
sudo apt-get install psycopg2
```
on remote server
``` 
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt install python3-pip
```

###Other links
https://github.com/mailgun/transactional-email-templates


