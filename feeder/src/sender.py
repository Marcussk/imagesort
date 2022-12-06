import argparse
import asyncio
import json
import sys
from typing import Any
from uuid import uuid4
import os
from pathlib import Path

from aio_pika import Message, connect

configuration = {
    "username": os.environ["RABBITMQ_USERNAME"],
    "password": os.environ["RABBITMQ_PASSWORD"],
    "hostname": os.environ["RABBITMQ_HOSTNAME"],
    "queue_name": "imagesort.input",
}



async def process_file(config: dict[str, Any], file_name: str) -> None:
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

async def process_folder(config: dict[str, Any], input_path: str) -> None:
    image_folder = Path(input_path).glob("*")
    folder_files = {path for path in image_folder if path.is_file()}
    for path in folder_files:
        await process_file(config, str(path.name))

async def main(directory_path: str) -> None:
    await process_folder(configuration, directory_path)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "-d",
        dest="directory",
        help="Path to directory containing images for sorting.")
    args = argument_parser.parse_args()
    if not args.directory:
        sys.exit("No directory path argument specified. See --help for usage.")
    asyncio.run(main(args.directory))
