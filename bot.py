#!/usr/bin/env python3

from os import environ
from flask import Flask
from flask import request

from webex import validate_webhook_registration
from webex import process_webhook_payload

import heroku


api = Flask(__name__)


@api.route('/', methods=['GET'])
def index():
    app_name = environ.get('HEROKU_APP_NAME')
    return f'App {app_name}'


@api.route('/webex-webhook', methods=['POST'])
def webex_webhook():
    webhook_data = request.json
    process_webhook_payload(webhook_data)
    return "<h1>Received</h1>"


def application():
    room_title = environ.get('WEBEX_TEAMS_ROOM_TITLE')
    webhook_url = heroku.get_web_url()
    validate_webhook_registration(room_title, webhook_url)
    return api


# This block is for local Flask execution
if __name__ == '__main__':
    application()
    api.debug = True
    api.run(host='127.0.0.1', port=5001)
