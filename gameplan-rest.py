from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
