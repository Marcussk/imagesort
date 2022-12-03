import asyncio
import json
from datetime import datetime
from uuid import uuid4

from aio_pika import Message, connect

cfg = {
    "username": "guest",
    "password": "guest",
    "hostname": "localhost",
    "queue_name": "imagesort.sorted",
}

async def main(config) -> None:
    connection = await connect(f"amqp://{config['username']}:{config['password']}@{config['hostname']}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(config["queue_name"])
        timestamp = datetime.now().isoformat()
        message_body: bytes = (json.dumps(
                {
                    "inserted_timestamp": timestamp,
                    "request_id": str(uuid4()),
                    "sort_key": "XXAAXX"
                }
            )).encode("utf-8")
        await channel.default_exchange.publish(
            Message(message_body),
            routing_key=queue.name,
        )
        print(message_body)


if __name__ == "__main__":
    asyncio.run(main(cfg))
