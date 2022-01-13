#!/usr/bin/env python3

import asyncio
import websockets

import wsconfig


async def produce(
    message: str, host: str, port: int
):
    async with websockets.connect(f'ws://{host}:{port}') as ws:
        await ws.send(message)
        return_comms = await ws.recv()

    return return_comms


def relay_command_message(message: str):
    return_comms = asyncio.run(
        produce(message, host=wsconfig.ws_host, port=wsconfig.ws_port)
    )

    return return_comms
