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

    async def start(self) -> None:
        self.consumer = ImageInputConsumer(self.config["consumer"], self.process_image)
        self.producer = ImageSortedProducer(self.config["producer"])
        await self.consumer.start()
        await self.producer.start()

    async def run(self) -> None:
        assert self.consumer
        await self.consumer.consume()

    async def process_image(self, input_message: ImageInputMessage) -> None:
        assert self.producer
        print(f"Processing {input_message.request_id}")

        image_path = self.dump_folder / input_message.file_path
        mean_color: str = self.get_mean_color(str(image_path))

        print(f"Sending to dump {input_message.request_id}")
        await self.producer.send(ImageSortedMessage(input_message.request_id, mean_color, input_message.file_path))
        print(f"Finished processing {input_message.request_id}")

    def get_mean_color(self, file_path: str) -> str:
        # pylint: disable=no-member
        image = cv2.imread(file_path)
        # opencv loads in BGR mode by default
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        average_color = image.mean(axis=0).mean(axis=0)
        normalized_color = tuple(round(channel) for channel in average_color)
        return rgb_to_hex(normalized_color)
