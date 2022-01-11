#!/usr/bin/env python

from os import environ
from flask import Flask
from flask import request
from webexteamssdk import WebexTeamsAPI
from webexteamssdk.models.immutable import Webhook, Room, Message

api = Flask(__name__)
webex = WebexTeamsAPI()

# TODO: Convert this hack to click or typer
def project_list():
    pass


def scenario_list():
    pass


supported_commands = {
    'project': {
        'list': project_list,
    },
    'scenario': {
        'list': scenario_list,
    }
}


def help():
    lines = []
    lines.append('Supported commands are:')

    for resource in supported_commands:
        for cmds in supported_commands[resource]:
            lines.append(
                f'\t{resource} {cmds} [args]'
            )

    return '\n'.join(lines)


@api.route('/', methods=['GET'])
def index():
    app_name = environ.get('HEROKU_APP_NAME')
    return f'App {app_name}'


@api.route('/webex-webhook', methods=['POST'])
def webex_webhook():
    webhook_data = request.json
    process_webhook_payload(webhook_data)
    return "<h1>Received</h1>"


def send_webex_message(roomId, parentId, text):
    webex.messages.create(roomId=roomId, parentId=parentId, text=text)


# Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL01FU1NBR0UvOTQxMjNmOTAtNzI2NS0xMWVjLTk4MTYtMGRhYzM4ZmViYzVm
def process_command_message(cmd_message: Message):
        # user = message.personEmail
        # command_message = message.text
        # roomId = message.roomId

    # First word is the Bot name... for now, hardcode "Lab", splice it out
    words = cmd_message.text[3:].split()

    # Special case: help
    if words[0] == 'help':
        result = help()

        send_webex_message(
            roomId = cmd_message.roomId,
            parentId = cmd_message.id,
            text = result
        )

        return

    # Pattern:  resource action arguments
    if words[0] not in supported_commands:
        error_message = f'Resource {words[0]} not recognized from: ' + str(cmd_message.text[3:])

        send_webex_message(
            roomId = cmd_message.roomId,
            parentId = cmd_message.id,
            text = error_message
        )

        return

    if len(words) == 1:
        error_message = f'No command provided for resource {words[0]}'

        send_webex_message(
            roomId = cmd_message.roomId,
            parentId = cmd_message.id,
            text = error_message
        )

        return

    if words[1] not in supported_commands[words[0]]:
        error_message = f'Command {words[1]} not recognized for resource {words[0]}'

        send_webex_message(
            roomId = cmd_message.roomId,
            parentId = cmd_message.id,
            text = error_message
        )

        return

    send_webex_message(
        roomId = cmd_message.roomId,
        parentId = cmd_message.id,
        text = f'Received resource {words[0]} with cmd/args {words[1:]}'
    )

    # Call the function pointed to by the dictionary
    command_parse = supported_commands[words[0]][words[1]]

    if len(words) > 2:
        command_parse(words[2:])
    else:
        command_parse()

    return


def process_webhook_payload(payload):

    # For this MVP, we are focused on Webhooks for created messages to the bot
    if payload['resource'] != 'messages':
        return

    if payload['event'] != 'created':
        return

    # Go fetch the message related to the webhook
    message: Message = webex.messages.get(payload['data']['id'])

    # Parse and process the message
    process_command_message(message)

    return


def get_webex_room_id(room_title):
    # Get roomID for the room
    room_list: list(Room) = webex.rooms.list()

    # Search through the list to find all room IDs that match the title
    all_room_ids = [
        room.id
        for room in room_list
        if room.title == room_title
    ]

    # We should only find one (application requiremes unique titles)
    if len(all_room_ids) > 1:
        raise Exception(
                        f'Duplicate rooms found for {room_title}',
                        list(room_list)
                        )

    return all_room_ids[0] if len(all_room_ids) else 0


def get_webhook_name(room_title, webhook_resource, webhook_event):
    return f'{webhook_resource}:{webhook_event} for "{room_title}"'


def get_webex_webhook(webhook_name) -> Webhook:
    """
    Get the webhooks that are specific to the specified room
    """
    webhooks: list(Webhook) = webex.webhooks.list()

    all_webhooks = [
        hook for hook in webhooks if hook.name == webhook_name
    ]

    # We should only find one (application requires unique titles)
    if len(all_webhooks) > 1:
        raise Exception(
                        f'Duplicate webhooks found for {webhook_name}',
                        list(webhooks)
                        )

    return all_webhooks[0] if len(all_webhooks) else None


def get_heroku_url(api_endpoint='/webex-webhook'):
    app_name = environ.get('HEROKU_APP_NAME')
    if not app_name:
        raise Exception(f'App name not set? "{app_name}"')

    return f'https://{app_name}.herokuapp.com{api_endpoint}'


def validate_webhook_registration(room_title):
    # Get the target room ID
    room_id = get_webex_room_id(room_title)

    # (FUTURE) Create room if doesn't exist
    if room_id == 0:
        raise Exception(f'"{room_title}" does not exist')

    # Determine the webhook name
    webhook_resource = 'messages'
    webhook_event = 'created'
    webhook_name = get_webhook_name(
                        room_title, webhook_resource, webhook_event
                    )

    # Fetch the existing webhook, if created
    webhook = get_webex_webhook(webhook_name)

    # Get application URL
    app_url = get_heroku_url()
    webhook_filter = f'roomId={room_id}&mentionedPeople=me'

    # If no existing webhook, simply create it
    if not webhook:
        webhook: Webhook = webex.webhooks.create(
            webhook_name, app_url, webhook_resource, webhook_event,
            webhook_filter
        )

        print('Created new webhook', str(webhook))
        return

    # Validate URL (may have changed because of new build) and status
    if (webhook.targetUrl != app_url) or (webhook.status == 'inactive'):
        updated_webhook: Webhook = webex.webhooks.update(
            webhook.id, name=webhook.name, targetUrl=app_url, status='active'
        )
        print('Updated webhook')
        print(str(webhook))
        print(str(updated_webhook))

    return


def application():
    room_title = environ.get('WEBEX_TEAMS_ROOM_TITLE')
    validate_webhook_registration(room_title)
    return api


# This block is for local Flask execution
if __name__ == '__main__':
    application()
    api.debug = True
    api.run(host='127.0.0.1', port=5001)
