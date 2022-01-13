#!/usr/bin/env python3

from webexteamssdk import WebexTeamsAPI
from webexteamssdk.models.immutable import Webhook, Room, Message
from relay import relay_command_message

webex = WebexTeamsAPI()


def process_webhook_payload(payload):

    # For this MVP, we are focused on Webhooks for created messages to the bot
    if payload['resource'] != 'messages':
        return

    if payload['event'] != 'created':
        return

    # Go fetch the message related to the webhook
    message: Message = webex.messages.get(payload['data']['id'])

    # Send the message downstream via websocket to get parsed
    return_message = relay_command_message(message.text)

    webex.messages.create(
        roomId=message.roomId, parentId=message.parentId, text=return_message
    )

    return


# Code below is for initializing/updating the WebEx webhook for this bot


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


def validate_webhook_registration(room_title, app_url):
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
