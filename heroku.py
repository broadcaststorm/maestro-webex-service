#!/usr/bin/env python3


from os import environ


def get_local_port():
    local_port = environ.get('PORT')
    if not local_port:
        raise Exception(f'PORT not set? "{local_port}"')

    return str(local_port)


def get_web_url(api_endpoint='/webex-webhook'):
    app_name = environ.get('HEROKU_APP_NAME')
    if not app_name:
        raise Exception(f'App name not set? "{app_name}"')

    return f'https://{app_name}.herokuapp.com{api_endpoint}'


def get_ws_host():
    ws_host = environ.get('WEBEX_RELAY_HOST')
    if not ws_host:
        raise Exception(f'WEBEX_RELAY_HOST not set? "{ws_host}"')

    return f'{ws_host}.herokuapp.com'


def get_ws_port():
    ws_port = environ.get('WEBEX_RELAY_PORT')
    if not ws_port:
        raise Exception(f'WEBEX_RELAY_PORT not set? "{ws_port}"')

    return str(ws_port)


def get_ws_url():
    ws_host = get_ws_host()
    ws_port = get_ws_port()

    return f'ws://{ws_host}:{ws_port}/'
