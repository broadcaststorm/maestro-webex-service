#!/usr/bin/env python3


import os
import json
import logging

from copy import deepcopy
from typing import List

import redis
from fastapi import HTTPException

from models import MessageSummary


class message_processor:
    def process_message(self, msg_id, msg_text, msg_email):
        pass

    def get_next_message(self) -> MessageSummary:
        pass

    def get_all_messages(self) -> List[MessageSummary]:
        pass


class message_store(message_processor):
    """
    /counter/start tracks the start of the "list" (the entry "before" the start)
    /counter/end tracks the end of the "list"
    - end-start = number of messages stored.
    - start+1 is first available message.

    /message/index is message number "index"
    """
    def __init__(self, url=None):
        self.url = url
        self.redis = redis.from_url(self.url, decode_responses=True)

        # Reset redis get counter
        self.set_start('0')
        self.set_end('0')

    def set_start(self, value):
        return self.redis.set(name='/counter/start', value=value)

    def set_end(self, value):
        return self.redis.get(name='/counter/end', value=value)

    def get_start(self):
        return self.redis.get(name='/counter/start')

    def get_end(self):
        return self.redis.get(name='/counter/end')

    def set_message(self, index, value):
        key = f'/message/{index}'
        self.redis.set(name=key, value=value)
        logging.info(f'{key}: {value}')

    def get_message(self, index):
        key = f'/message/{index}'
        return self.redis.get(name=key)

    def get_indexes(self):
        start = int(self.get_start())
        end = int(self.get_end())

        if start == end:
            raise HTTPException(
                status_code=404,
                detail='Message List Empty'
            )

        return start, end

    def process_message(self, msg_id, msg_text, msg_email):
        end = self.get_end()
        index = str(int(end) + 1)

        data = MessageSummary(id=msg_id, text=msg_text, email=msg_email)
        value = json.dumps(data.dict())

        self.set_message(index, value)
        self.set_end(index)

    def get_next_message(self) -> MessageSummary:
        start, end = self.get_indexes()

        index = start + 1
        value = self.get_message(index)
        data = json.loads(value)
        message = MessageSummary(**data)

        self.set_start(str(index))
        return message

    def get_all_messages(self) -> List[MessageSummary]:
        start, end = self.get_indexes()

        results: List[MessageSummary] = list()

        while (start < end):
            start = start + 1
            value = self.get_message(start)
            data = json.loads(value)

            results.append(MessageSummary(**data))

        self.set_start(start)
        return results


class message_buffer(message_processor):
    def __init__(self):
        self.messages: List[MessageSummary] = list()

    def process_message(self, msg_id, msg_text, msg_email):
        self.messages.append(
            MessageSummary(id=msg_id, text=msg_text, email=msg_email)
        )

        logging.info(f'Proc: Message buffer size: {len(self.messages)}')

    def get_next_message(self) -> MessageSummary:
        logging.info(f'Proc: Message buffer size: {len(self.messages)}')

        if len(self.messages) == 0:
            raise HTTPException(
                status_code=404,
                detail='Message List Empty'
            )

        return self.messages.pop(0)

    def get_all_messages(self) -> List[MessageSummary]:
        logging.info(f'Proc: Message buffer size: {len(self.messages)}')

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

    if service_type == 'REDIS':
        redis_url = os.environ.get('REDIS_URL')
        return message_store(url=redis_url)

    raise Exception('Unknown message relay type')
