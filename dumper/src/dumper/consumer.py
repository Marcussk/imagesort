import json
import logging
from asyncio import Future
from typing import Any, Awaitable, Callable

from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .models import ImageSortedMessage, ImageSortedParsingError

SortedMessageHandler = Callable[[ImageSortedMessage], Awaitable[None]]

RABBITMQ_CONNECTION_TIMEOUT = 60


class ImageSortedConsumer:
    def __init__(self, config: dict[str, Any], message_handler: SortedMessageHandler) -> None:
        self.queue_name: str = config["queue_name"]
        self.message_handler: SortedMessageHandler = message_handler
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}"
        self.connection: AbstractConnection | None = None
        self.logger = logging.getLogger()

    async def stop(self) -> None:
        if self.connection:
            await self.connection.close()

    async def consume(self) -> None:
        self.logger.info("Consuming ImageSortedMessage")
        self.connection = await connect_robust(self.connection_string, timeout=RABBITMQ_CONNECTION_TIMEOUT)
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
            model = ImageSortedMessage.from_dict(message_json)
            self.logger.debug("Parsed ImageSortedMessage %s", model.request_id)
            await self.message_handler(model)
        except ImageSortedParsingError:
            self.logger.exception("Could not parse message: %s", message)
