
from pathlib import Path
from typing import Any

from webcolors import hex_to_name

from .consumer import ImageSortedConsumer
from .models import ImageSortedMessage


class Dumper:
    def __init__(self, config: dict[str, Any]) -> None:
        self.dump_folder = Path(config["dump_folder"])
        self.consumer = ImageSortedConsumer(config["consumer"], self.process)

    async def start(self) -> None:
        await self.consumer.start()

    async def run(self) -> None:
        await self.consumer.consume()

    async def process(self, message: ImageSortedMessage) -> None:
        print(message)
        color_name = hex_to_name(message.mean_color)
        print(self.dump_folder / color_name)
