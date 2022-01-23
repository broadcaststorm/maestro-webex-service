#!/usr/bin/env python3

from os import environ
from flask import Flask
from flask import request

import webex
import heroku

rest_api = Flask(__name__)


def application():
    global webex_api

    global app_version
    global app_name
    global app_webhook_url

    app_version = '0.1.0'

    # Heroku setup
    app_name, app_webhook_url = heroku.initialization()

    # WebEx setup
    webex_api = webex.initialization(app_webhook_url)

    return rest_api


@rest_api.route('/', methods=['POST'])
def webex_webhook():
    webhook_data = request.json
    webex.process_webhook_payload(webex_api, webhook_data)
    return "<h1>Received</h1>"


@rest_api.route('/', methods=['GET'])
def index():
    app_name = environ.get('HEROKU_APP_NAME')
    return f'App {app_name}'


# This block is for local Flask execution
if __name__ == '__main__':
    api = application()
    api.debug = True
    api.run(host='127.0.0.1', port=5001)
