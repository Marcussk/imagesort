import argparse
import asyncio
import json
import sys
from typing import Any
from uuid import uuid4
import os

from aio_pika import Message, connect

cfg = {
    "username": os.environ["RABBITMQ_USERNAME"],
    "password": os.environ["RABBITMQ_PASSWORD"],
    "hostname": os.environ["RABBITMQ_HOSTNAME"],
    "queue_name": "imagesort.input",
}

async def main(config: dict[str, Any], file_name: str) -> None:
    connection = await connect(f"amqp://{config['username']}:{config['password']}@{config['hostname']}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(config["queue_name"])
        message_body: bytes = (json.dumps(
                {
                    "request_id": str(uuid4()),
                    "file_path": file_name
                }
            )).encode("utf-8")
        await channel.default_exchange.publish(
            Message(message_body),
            routing_key=queue.name,
        )
        print(message_body)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-f", dest="file_name", help="Path to image for sorting.")
    args = argument_parser.parse_args()
    if not args.file_name:
        sys.exit("No file_path argument specified. See --help for usage.")
    asyncio.run(main(cfg, args.file_name))
