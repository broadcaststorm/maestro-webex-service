#!/usr/bin/env python

from os import environ
from flask import Flask, request

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index(): 
    app_name = environ.get('HEROKU_APP_NAME')
    return f'App {app_name}'

# This block is for local Flask execution
if __name__ == '__main__':
    api.debug = True
    api.run()
