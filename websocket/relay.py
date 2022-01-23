#!/usr/bin/env python3

import asyncio
import websockets

import heroku


async def produce(
    message: str, host: str, port: int
):
    async with websockets.connect(f'ws://{host}:{port}') as ws:
        await ws.send(message)
        return_comms = await ws.recv()

    return return_comms


def relay_command_message(message: str):
    ws_host = heroku.get_ws_host()
    ws_port = heroku.get_ws_port()

    return_comms = asyncio.run(
        produce(message, host=ws_host, port=ws_port)
    )

    return return_comms
