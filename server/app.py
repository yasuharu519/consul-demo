import os
import json
import socket
from time import sleep

import requests
from flask import Flask, render_template

app = Flask(__name__)

BASE_CONSUL_URL = 'http://consul:8500'

SERVICE_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8080

@app.route('/')
def index():
    color = os.environ.get('COLOR', "#000")
    return render_template('index.html',
                           address=SERVICE_ADDRESS,
                           color=color)

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
        'Name': 'server',
        'Tags': ['flask'],
        'Address': SERVICE_ADDRESS,
        'Port': 8080,
        'Check': {
            'http': 'http://{address}:{port}/health'.format(address=SERVICE_ADDRESS, port=PORT),
            'interval': '2s'
        }
    }
    app.logger.debug('Service registration parameters: ', data)
    res = requests.put(
        url,
        data=json.dumps(data)
    )
    return res.text


if __name__ == '__main__':
    sleep(3)
    try:
        app.logger.debug(register())
    except:
        app.logger.debug('Something wrong happened!')
        pass
    app.run(debug=True, host="0.0.0.0", port=PORT)
