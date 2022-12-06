import json
import logging
from asyncio import Future
from typing import Any, Awaitable, Callable

from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .models import ImageInputMessage, ImageInputParsingError

InputMessageHandler = Callable[[ImageInputMessage], Awaitable[None]]

RABBITMQ_CONNECTION_TIMEOUT = 60


class ImageInputConsumer:
    def __init__(self, config: dict[str, Any], message_handler: InputMessageHandler) -> None:
        self.queue_name: str = config["queue_name"]
        self.message_handler: InputMessageHandler = message_handler
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}/"
        self.connection: AbstractConnection | None = None
        self.logger = logging.getLogger()

    async def start(self) -> None:
        self.logger.info("Starting ImageInputConsumer")
        self.connection = await connect_robust(self.connection_string, timeout=RABBITMQ_CONNECTION_TIMEOUT)

    async def consume(self) -> None:
        self.logger.info("Consuming ImageInputMessage")
        assert self.connection
        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(self.queue_name)
            await queue.consume(self.on_message, no_ack=True)
            await Future()

    async def stop(self) -> None:
        if self.connection:
            await self.connection.close()

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        """
        Parses incoming message into model and passes it to handler for processing.
        """
        self.logger.debug("Processing message")
        try:
            model = ImageInputMessage.from_dict(json.loads(message.body.decode("utf-8")))
            self.logger.debug("Parsed message: %s", model.request_id)
            await self.message_handler(model)
        except ImageInputParsingError:
            self.logger.exception("Exception when parsing message: %s", message)
