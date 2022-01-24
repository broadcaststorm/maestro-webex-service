#!/usr/bin/env python3


import os
import logging
from copy import deepcopy
from typing import List

from fastapi import HTTPException

from models import MessageSummary


class message_processor:
    def process_message(self, msg_id, msg_text, msg_email):
        pass

    def get_next_message(self) -> MessageSummary:
        pass

    def get_all_messages(self) -> List[MessageSummary]:
        pass


class message_buffer(message_processor):
    def __init__(self):
        self.messages: List[MessageSummary] = list()

    def process_message(self, msg_id, msg_text, msg_email):
        self.messages.append(
            MessageSummary(id=msg_id, text=msg_text, email=msg_email)
        )

        logging.info('Message buffer size: ', len(self.messages))

    def get_next_message(self) -> MessageSummary:
        logging.info('Message buffer size: ', len(self.messages))

        if len(self.messages) == 0:
            raise HTTPException(
                status_code=404,
                detail='Message List Empty'
            )

        return self.messages.pop(0)

    def get_all_messages(self) -> List[MessageSummary]:
        logging.info('Message buffer size: ', len(self.messages))

        if len(self.messages) == 0:
            raise HTTPException(
                status_code=404,
                detail='Message List Empty'
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
