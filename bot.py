#!/usr/bin/env python3


from typing import List

from fastapi import FastAPI, HTTPException
from models import Version, WebhookEvent, MessageSummary

import webex
import heroku
import relay


def application():
    global webex_api
    global api

    global relay_service
    global app_version
    global app_name
    global app_webhook_url

    api = FastAPI()
    app_version = '0.1.1'

    # Heroku setup
    app_name, app_webhook_url = heroku.initialization()

    # WebEx setup
    webex_api = webex.initialization(app_webhook_url)

    # Message Relay setup
    relay_service = relay.initialization()

    return api


# Entry point for gunicorn/uvicorn
app = application()


@api.get('/')
def get_app_name():
    global app_name
    return { "message": f'App {app_name}' }


@api.post('/')
def post_webhook_data(event: WebhookEvent):
    global webex_api
    global relay_service

    # For this MVP, we are focused on Webhooks for created messages to the bot
    if event.resource != 'messages':
        return

    if event.event != 'created':
        return

    try:
        webex.process_webhook_payload(webex_api, relay_service, event.data.id)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=400, detail='Generic failure')


@api.get('/version', response_model=Version)
def get_version():
    global app_version
    return Version(version=app_version)


# REST API below are for polling from lab environments
@api.get('/messages', response_model=List[MessageSummary])
def get_all_messages():
    global relay_service

    return relay_service.get_all_messages()


@api.get('/messages/next', response_model=MessageSummary)
def get_next_messages():
    global relay_service

    return relay_service.get_next_message()


# This block is for local execution
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
