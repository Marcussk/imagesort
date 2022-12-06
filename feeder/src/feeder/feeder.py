
from typing import Any
from .producer import ImageInputProducer
from .models import ImageInputMessage
from pathlib import Path
import logging
import asyncio

class Feeder:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.producer: ImageInputProducer | None = None
        self.dump_folder = Path(config["dump_folder"])
        self.dump_folder.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(level=config["log_level"])
        self.logger = logging.getLogger()
        self.logger.info("Feeder initialized for folder %s", self.dump_folder)

    async def start(self) -> None:
        self.logger.info("Starting Feeder")
        self.producer = ImageInputProducer(self.config["producer"])
        await self.producer.start()

    async def run(self) -> None:
        self.logger.info("Running Feeder")
        while True:
            await self.process_folder()
            await asyncio.sleep(self.config["backoff_time"])

    async def process_file(self, file_name: str) -> None:
        self.logger.info("Processing file: %s", file_name)
        assert self.producer
        message = ImageInputMessage.from_file_path(file_name)
        await self.producer.send(message)
        self.logger.info("Request %s fed to sorter", message.request_id)

    async def process_folder(self) -> None:
        self.logger.info("Checking folder")
        folder_files = {path for path in self.dump_folder.glob("*") if path.is_file()}
        for path in folder_files:
            await self.process_file(str(path.name))