# imports
from flask import Flask, request, make_response
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

# custom response
@app.route('/hello', methods=['POST', 'GET'])
def hello():
    response = make_response('Hello World\n')
    response.status_code = 202
    response.headers['content-type'] = 'text/plain'
    return response
    # 201 is successful req and new rsc created
    # 202 req accepted; processing not compelted. async tasks
    # 404 not found
    # 500 internal server error
    # 501 not implemented
    # 936 unknown
    # 200 wored; 300 redirect; 400 server errror; 500 server error
    # if request.method == 'GET':
    #     return 'You made a GET request\n'
    # elif request.method == 'POST':
    #     return 'You made a POST request\n'
    # else:
    #     return 'You shouldn\'t see this message.\n'
    # return "Hello World"

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}"

@app.route('/add/<int:number1>/<int:number2>')
def add(number, number2):
    # number1=int(number1) ggggggggg
    return f'{number1}+{number2}={number1+number2}'

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f"{greeting}, {name}"
    else:
        return "Some parameters are missing"

#each. app route is end route. 1 request only
#curl sends reqs consued


    # return str(requests.args) new jeans ohhh



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
