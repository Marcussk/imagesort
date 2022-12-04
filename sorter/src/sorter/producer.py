import json
from dataclasses import asdict
from typing import Any

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractConnection

from .models import ImageSortedMessage


class ImageSortedProducer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.queue_name: str = config["queue_name"]
        self.connection_string: str = f"amqp://{config['username']}:{config['password']}@{config['hostname']}/"
        print(self.connection_string)
        self.connection: AbstractConnection | None = None

    async def start(self) -> None:
        print("Connecting to: ", self.connection_string)
        self.connection = await connect_robust(self.connection_string, timeout=60)

    async def send(self, message: ImageSortedMessage) -> None:
        assert self.connection
        # TODO: connection persistent
        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(self.queue_name)
            message_body = (json.dumps(asdict(message))).encode("utf-8")
            await channel.default_exchange.publish(
                Message(message_body),
                routing_key=queue.name,
            )
            print(message_body)