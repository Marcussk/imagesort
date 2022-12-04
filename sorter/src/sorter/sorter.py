from typing import Any

from .consumer import ImageInputConsumer
from .models import ImageInputMessage, ImageSortedMessage
from .producer import ImageSortedProducer


class Sorter:
    def __init__(self, config: dict[str, Any]) -> None:
        self.consumer = ImageInputConsumer(config["consumer"], self.process_image)
        self.producer = ImageSortedProducer(config["producer"])

    async def process_image(self, input_message: ImageInputMessage) -> None:
        mean_color: str = self.get_mean_color(input_message)
        sorted_message = ImageSortedMessage(input_message.request_id, mean_color)
        await self.producer.send(sorted_message)

    def get_mean_color(self, input_message: ImageInputMessage) -> str:
        with open(input_message.file_path, "r", encoding="utf-8") as image_file:
            # TODO: properly get mean color
            print(image_file.read()[:64])
        return "#FF0000"