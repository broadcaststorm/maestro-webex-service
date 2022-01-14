#!/usr/bin/env python3


from os import environ


def get_heroku_web_url(api_endpoint='/webex-webhook'):
    app_name = environ.get('HEROKU_APP_NAME')
    if not app_name:
        raise Exception(f'App name not set? "{app_name}"')

    return f'https://{app_name}.herokuapp.com{api_endpoint}'


def get_ws_host():
    app_name = environ.get('HEROKU_APP_NAME')
    if not app_name:
        raise Exception(f'App name not set? "{app_name}"')

    return f'{app_name}.herokuapp.com'


def get_ws_port():
    return '54321'


def get_ws_url():
    ws_host = get_ws_host()
    ws_port = get_ws_port()

    return f'ws://{ws_host}:{ws_port}/'
