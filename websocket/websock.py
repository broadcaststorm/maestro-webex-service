#!/usr/bin/env python3
"""
This module focuses on establishing the websocket service with which
to communicate bot command directives into the private network lab
service.

Credit: bulk of this code originates from the following blog post, by
Dieter Jordens (https://www.dieterjordens.com):

https://betterprogramming.pub/how-to-create-a-websocket-in-python-b68d65dbd549

"""

import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol

import heroku


logging.basicConfig(level=logging. INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait(
                [client.send(message) for client in self.clients]
            )

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)


if __name__ == '__main__':
    print('Starting web socket server...')

    server = Server()
    start_server = websockets.serve(
        server.ws_handler, '', heroku.get_local_port()
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
