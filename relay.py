#!/usr/bin/env python3


from http.client import HTTPException
import os
from copy import deepcopy
from typing import List

from models import MessageSummary


class message_buffer:
    def __init__(self):
        self.messages: List[MessageSummary] = list()

    def process_message(self, msg_id, msg_text, msg_email):
        self.messages.append(
            MessageSummary(id=msg_id, text=msg_text, email=msg_email)
        )

    def get_next_message(self) -> MessageSummary:
        if len(self.messages) == 0:
            raise HTTPException(
                status_code=404,
                status_message='Message List Empty'
            )

        return self.messages.pop(0)

    def get_all_messages(self) -> List[MessageSummary]:
        if len(self.messages) == 0:
            raise HTTPException(
                status_code=404,
                status_message='Message List Empty'
            )

        msgs = deepcopy(self.messages)
        self.messages = list()
        return msgs


def initialization():
    # Check environment variable to determine which message class
    service_type = os.environ.get('WEBEX_RELAY_TYPE', 'BUFFER')

    if service_type == 'BUFFER':
        return message_buffer()

    raise Exception('Unknown message relay type')
