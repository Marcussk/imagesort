import json
from asyncio import Future
from typing import Any, Awaitable, Callable

from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .models import ImageSortedMessage, ImageSortedParsingError

SortedMessageHandler = Callable[[ImageSortedMessage], Awaitable[None]]


class ImageSortedConsumer:
    def __init__(self, config: dict[str, Any], message_handler: SortedMessageHandler) -> None:
        self.queue_name: str = config["queue_name"]
        self.message_handler: SortedMessageHandler = message_handler
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}"
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
            message_json = json.loads(message.body.decode("utf-8"))
            print(message_json)
            model = ImageSortedMessage.from_json(message_json)
            await self.message_handler(model)
        except ImageSortedParsingError as exception:
            print(exception)
            print(f"Could not parse message: {message} {message.body.decode('utf-8')}")
