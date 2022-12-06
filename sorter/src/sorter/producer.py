import json
import logging
from dataclasses import asdict
from typing import Any

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractConnection

from .models import ImageSortedMessage

RABBITMQ_CONNECTION_TIMEOUT = 60


class ImageSortedProducer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.queue_name: str = config["queue_name"]
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}/"
        self.connection: AbstractConnection | None = None
        self.logger = logging.getLogger()

    async def stop(self) -> None:
        if self.connection:
            await self.connection.close()

    async def send(self, message: ImageSortedMessage) -> None:
        self.logger.debug("Sending message: %s", message.request_id)
        self.connection = await connect_robust(self.connection_string, timeout=RABBITMQ_CONNECTION_TIMEOUT)
        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(self.queue_name)
            message_body = (json.dumps(asdict(message))).encode("utf-8")
            await channel.default_exchange.publish(
                Message(message_body),
                routing_key=queue.name,
            )
