import threading
import time
import requests


def run(n):
    print('task', n)
    r = requests.get('http://127.0.0.1:5000/index')
    print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), r.content)


if __name__ == "__main__":
    for i in range(20):
        t = threading.Thread(target=run, args=("t- %s"%i,))
        t.start()
