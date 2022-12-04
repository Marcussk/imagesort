import json
from asyncio import Future
from typing import Any, Awaitable, Callable

from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .models import ImageInputMessage, ImageInputParsingError

InputMessageHandler = Callable[[ImageInputMessage], Awaitable[None]]

class ImageInputConsumer:
    def __init__(self, config: dict[str, Any], message_handler: InputMessageHandler) -> None:
        self.queue_name: str = config["queue_name"]
        self.message_handler: InputMessageHandler = message_handler
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}/"
        print(self.connection_string)
        self.connection: AbstractConnection | None = None

    async def start(self) -> None:
        print("Connecting to: ", self.connection_string)
        self.connection = await connect_robust(self.connection_string, timeout=60)

    async def consume(self) -> None:
        assert self.connection
        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(self.queue_name)
            await queue.consume(self.on_message, no_ack=True)
            await Future()

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        """
        Parses incoming message into model and passes it to handler for processing.
        """
        try:
            # FIXME: Invalid json
            model = ImageInputMessage.from_json(json.loads(message.body.decode("utf-8")))
            await self.message_handler(model)
        except ImageInputParsingError:
            print(f"Could not parse message: {message}")
        