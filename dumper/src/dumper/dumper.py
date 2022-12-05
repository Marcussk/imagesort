
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
        color_name = self.get_color_name(message.mean_color)
        self.dump_file(message.file_path, color_name)
        print(f"Finished: {message.request_id}")

    def get_color_name(self, hex_color: str) -> str:
        """
        Gets color name for input hex_color.

        If color name does not exists hex_color is used. 
        """
        try:
            color_name = hex_to_name(hex_color)
        except ValueError as exception:
            print(f"Cannot get name for {hex_color}: {exception}")
            color_name = hex_color.lstrip("#")
        return color_name

    def dump_file(self, original_file_path: str, color_name: str) -> None:
        """
            Moves file into correct folder according to its sorting.

            If file exists, it is not moved.
        """
        target_folder = self.dump_folder / color_name
        target_folder.mkdir(parents=True, exist_ok=True)

        target_file_path = target_folder / original_file_path
        image_file_path = self.dump_folder / original_file_path

        try:
            image_file_path.rename(target_file_path)
        except FileExistsError:
            print("File already exists can't replace.")
