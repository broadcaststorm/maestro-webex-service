#!/usr/bin/env python3

from flask import Flask
from flask import request

import webex
import heroku
from relay import message_service


# Global Variable Setup
rest_api = Flask(__name__)
webex_api = None
relay_service = None


def application():
    global webex_api
    global relay_service

    global app_version
    global app_name
    global app_webhook_url

    app_version = '0.1.0'

    # Heroku setup
    app_name, app_webhook_url = heroku.initialization()

    # WebEx setup
    webex_api = webex.initialization(app_webhook_url)

    return rest_api


@rest_api.route('/', methods=["GET", "POST"])
def index():
    global relay_service
    global app_name

    if request.method == "POST":
        webhook_data = request.json
        webex.process_webhook_payload(webex_api, relay_service, webhook_data)
        return "<h1>Received</h1>"

    if request.method == "GET":
        return f'App {app_name}'


@rest_api.route('/version', methods=["GET"])
def version():
    global app_version
    return str(app_version)


# This block is for local Flask execution
if __name__ == '__main__':
    api = application()
    api.debug = True
    api.run(host='127.0.0.1', port=5001)
