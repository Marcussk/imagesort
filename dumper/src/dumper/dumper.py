import json
from asyncio import Future
from pathlib import Path
from typing import Any, Awaitable, Callable

from aio_pika import connect
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .models import ImageSortedMessage, MessageParsingException

SortedMessageHandler = Callable[[ImageSortedMessage], Awaitable[None]]


class Consumer:
    def __init__(self, config: dict[str, Any], message_handler: SortedMessageHandler) -> None:
        self.queue_name: str = config["queue_name"]
        self.message_handler: SortedMessageHandler = message_handler
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}/"
        print(self.connection_string)
        self.connection: AbstractConnection | None = None

    async def start(self) -> None:
        self.connection = await connect(self.connection_string)

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
            model = ImageSortedMessage.from_json(json.loads(message.body.decode("utf-8")))
            await self.message_handler(model)
        except MessageParsingException:
            print(f"Could not parse message: {message}")
        


class Dumper:
    def __init__(self, config: dict[str, Any]) -> None:
        self.dump_folder: Path = Path(config["dump_folder"])
        self.consumer = Consumer(config["consumer"], self.process)

    async def start(self) -> None:
        await self.consumer.start()

    async def run(self) -> None:
        await self.consumer.consume()

    async def process(self, message: ImageSortedMessage) -> None:
        print(message)
        print(self.dump_folder / message.sort_key)
