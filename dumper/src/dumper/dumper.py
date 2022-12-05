
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
        print(f"Saving {message.request_id}")
        print(message)
        color_name = hex_to_name(message.mean_color)
        self.dump_file(message.file_path, self.dump_folder / color_name)
        print(f"Finished: {message.request_id}")

    def dump_file(self, original_file_path: str, target_folder: Path):
        target_folder.mkdir(parents=True, exist_ok=True)
        image_file_path = self.dump_folder / original_file_path
        target_file_path = target_folder / original_file_path
        print(str(image_file_path), "->", target_file_path)
        image_file_path.rename(target_file_path)
