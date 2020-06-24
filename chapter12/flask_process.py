from flask import Flask
import time
import requests


app = Flask(__name__)


@app.route('/index')
def hello_world():
    print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), 'hello world')
    response = requests.get('http://www.baidu.com')
    time.sleep(10)
    return response


if __name__ == '__main__':

    app.run(threaded=False, processes=17)
