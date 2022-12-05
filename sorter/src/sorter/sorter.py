from typing import Any

from .consumer import ImageInputConsumer
from .models import ImageInputMessage, ImageSortedMessage
from .producer import ImageSortedProducer

import cv2
from webcolors import rgb_to_hex
from pathlib import Path


class Sorter:
    def __init__(self, config: dict[str, Any]) -> None:
        self.consumer = ImageInputConsumer(config["consumer"], self.process_image)
        self.producer = ImageSortedProducer(config["producer"])
        self.dump_folder = Path(config["dump_folder"])

    async def start(self) -> None:
        await self.consumer.start()
        await self.producer.start()

    async def run(self) -> None:
        await self.consumer.consume()

    async def process_image(self, input_message: ImageInputMessage) -> None:
        print(f"Processing {input_message.request_id}")
        image_path = self.dump_folder / input_message.file_path
        mean_color: str = self.get_mean_color(str(image_path))
        print(f"Sending to dump {input_message.request_id}")
        await self.producer.send(ImageSortedMessage(input_message.request_id, mean_color, input_message.file_path))
        print(f"Finished processing {input_message.request_id}")

    def get_mean_color(self, file_path: str) -> str:
        image = cv2.imread(file_path)
        # opencv loads in BGR mode by default
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        average_color = image.mean(axis=0).mean(axis=0)
        normalized_color = tuple(round(channel) for channel in average_color)
        return rgb_to_hex(normalized_color)
