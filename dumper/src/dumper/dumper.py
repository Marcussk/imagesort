
from pathlib import Path
from typing import Any

from .models import ImageSortedMessage
from .consumer import ImageSortedConsumer


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
        print(self.dump_folder / message.sort_key)
