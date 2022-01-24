#!/usr/bin/env python3


from os import environ

from webexteamssdk import WebexTeamsAPI
from webexteamssdk.models.immutable import Webhook, Room, Message


def process_webhook_payload(webex: WebexTeamsAPI, relay, msg_id: int):

    # Go fetch the message related to the webhook
    message: Message = webex.messages.get(msg_id)

    # Send the message downstream to get parsed. Rely on downstream
    # to communicate any results (given this could be stored messages)
    relay.process_message(
        msg_id=int(message.id),
        msg_text=str(message.text),
        msg_email=str(message.personEmail)
    )

    return


# Code below is for initializing/updating the WebEx webhook for this bot
def get_webhook_name(room_title, webhook_resource, webhook_event):
    return f'{webhook_resource}:{webhook_event} for "{room_title}"'


def get_webex_webhook(webex: WebexTeamsAPI, webhook_name) -> Webhook:
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


def get_webex_room_id(webex: WebexTeamsAPI, room_title):
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


def validate_webhook_registration(webex: WebexTeamsAPI, room_title, app_url):
    # Get the target room ID
    room_id = get_webex_room_id(webex, room_title)

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
    webhook = get_webex_webhook(webex, webhook_name)

    # Get application URL
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


def initialization(webhook_url: str):

    # Which room are we monitoring?
    webex_room_title = environ.get('WEBEX_TEAMS_ROOM_TITLE')
    if not webex_room_title:
        raise Exception('WEBEX_TEAMS_ROOM_TITLE env var is required.')

    # Make sure our secure token is loaded
    if not environ.get('WEBEX_TEAMS_ACCESS_TOKEN'):
        raise Exception('WEBEX_TEAMS_ACCESS_TOKEN env var is required.')

    # Load up WebexTeams API instance
    webex_api = WebexTeamsAPI(wait_on_rate_limit=True)

    # Does the room exist?
    webex_room_id = get_webex_room_id(webex_api, webex_room_title)
    if webex_room_id == 0:
        raise Exception('Room "{webex_room_title}" not found.')

    # Update the webhook information when we startup the bot service
    validate_webhook_registration(webex_api, webex_room_title, webhook_url)

    return webex_api, webex_room_title, webex_room_id
