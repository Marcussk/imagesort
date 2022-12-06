import logging
from pathlib import Path
from typing import Any

import cv2
from webcolors import rgb_to_hex

from .consumer import ImageInputConsumer
from .models import ImageInputMessage, ImageSortedMessage
from .producer import ImageSortedProducer


class Sorter:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.consumer: ImageInputConsumer | None = None
        self.producer: ImageSortedProducer | None = None
        self.dump_folder = Path(config["dump_folder"])
        self.dump_folder.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(level=config["log_level"])
        self.logger = logging.getLogger()

    async def start(self) -> None:
        self.logger.info("Starting sorter")
        self.consumer = ImageInputConsumer(self.config["consumer"], self.process_image)
        self.producer = ImageSortedProducer(self.config["producer"])
        await self.consumer.start()
        await self.producer.start()

    async def run(self) -> None:
        self.logger.info("Running sorter")
        assert self.consumer
        await self.consumer.consume()

    async def process_image(self, input_message: ImageInputMessage) -> None:
        assert self.producer
        self.logger.info("Processing %s", input_message.request_id)

        image_path = self.dump_folder / input_message.file_path
        if not image_path.exists():
            self.logger.error("Cannot load image at: %s from request %s, file does not exist", image_path, input_message.request_id)
            return 
        mean_color: str = self.get_mean_color(str(image_path))
        self.logger.info("Request %s mean color: %s", input_message.request_id, mean_color)

        await self.producer.send(ImageSortedMessage(input_message.request_id, mean_color, input_message.file_path))
        self.logger.info("Passed processing of request %s", input_message.request_id)

    def get_mean_color(self, file_path: str) -> str:
        # pylint: disable=no-member
        image = cv2.imread(file_path)
        # opencv loads in BGR mode by default
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        average_color = image.mean(axis=0).mean(axis=0)
        normalized_color = tuple(round(channel) for channel in average_color)
        return rgb_to_hex(normalized_color)
