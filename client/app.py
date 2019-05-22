import os
import json
import socket
import random
import atexit
from time import sleep

import requests
from flask import Flask, render_template

app = Flask(__name__)

BASE_CONSUL_URL = 'http://consul:8500'

# consul 登録したサービス名
SERVICE_NAME = 'client'
SERVICE_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8080

# アクセス先サービス名
SERVER_SERVICE_NAME = 'server'

@app.route('/')
def index():
    url = BASE_CONSUL_URL + '/v1/catalog/service/' + SERVER_SERVICE_NAME
    res = requests.get(url).json()
    choosed = random.choice(res)
    return requests.get("http://{}:{}".format(
        choosed.get("ServiceAddress"),
        choosed.get("ServicePort"))).text

@app.route('/health')
def health():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)

@app.route('/register')
def register():
    url = BASE_CONSUL_URL + '/v1/agent/service/register'
    data = {
        'Name': SERVICE_NAME,
        'Tags': ['flask'],
        'Address': SERVICE_ADDRESS,
        'Port': 8080,
        'Check': {
            'http': 'http://{address}:{port}/health'.format(address=SERVICE_ADDRESS, port=PORT),
            'interval': '10s'
        }
    }
    app.logger.debug('Service registration parameters: ', data)
    res = requests.put(
        url,
        data=json.dumps(data)
    )
    return res.text

@app.route('/deregister')
def deregister():
    url = BASE_CONSUL_URL + '/v1/agent/service/deregister/' + SERVICE_NAME
    app.logger.info('Service deregister: ', SERVICE_NAME)
    res = requests.put(url)
    return "ok" if res else "failed"

if __name__ == '__main__':
    sleep(3)
    try:
        app.logger.debug(register())
    except:
        app.logger.debug('Something wrong happened!')
        pass
    atexit.register(deregister)
    app.run(debug=True, host="0.0.0.0", port=PORT)
