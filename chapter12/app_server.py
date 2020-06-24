from flask import Flask
from flask import request, make_response, abort
print(__name__)
app = Flask(__name__)


def load_user(id):
    if id == 0:
        return None
    else:
        return 'MHT'


@app.route('/')
def index():
    print(request.headers)
    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    print(user)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user


@app.route('/user/<name>')
def run(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)


