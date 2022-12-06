import logging
from pathlib import Path
from typing import Any

from webcolors import hex_to_name

from .consumer import ImageSortedConsumer
from .models import ImageSortedMessage


class Dumper:
    """
    Consumes incoming `ImageSortedMessage`s and `process`es them by moving images into correct folder.
    Folder is assigned by converting mean color obtained from sorter.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config: dict[str, Any] = config
        self.dump_folder = Path(config["dump_folder"])
        self.dump_folder.mkdir(parents=True, exist_ok=True)
        self.consumer: ImageSortedConsumer | None = None
        logging.basicConfig(level=config["log_level"])
        self.logger = logging.getLogger()
        self.logger.info("Dumper initialized for folder %s", self.dump_folder)

    async def start(self) -> None:
        self.logger.info("Starting Dumper")
        self.consumer = ImageSortedConsumer(self.config["consumer"], self.process)

    async def run(self) -> None:
        self.logger.info("Running Dumper")
        assert self.consumer
        await self.consumer.consume()

    async def stop(self) -> None:
        if self.consumer:
            await self.consumer.stop()

    async def process(self, message: ImageSortedMessage) -> None:
        self.logger.info("Dumper processing %s", message.request_id)
        self.logger.debug("Message received: %s", message)
        color_name = self.get_color_name(message.mean_color)
        self.logger.info("Request %s final color name: %s", message.request_id, color_name)
        self.dump_file(message.file_path, color_name, message.request_id)

    def get_color_name(self, hex_color: str) -> str:
        """
        Gets color name for input hex_color.

        If color name does not exists hex_color is used.
        """
        try:
            color_name: str = hex_to_name(hex_color)
        except ValueError:
            self.logger.exception("Cannot get name for %s", hex_color)
            color_name = hex_color.lstrip("#")
        return color_name

    def dump_file(self, original_file_path: str, color_name: str, request_id: str) -> None:
        """
        Moves file into correct folder according to its sorting.

        If file exists, it is not moved.
        """
        target_folder = self.dump_folder / color_name
        target_folder.mkdir(parents=True, exist_ok=True)

        image_file_path = self.dump_folder / original_file_path
        if not image_file_path.exists():
            self.logger.error(
                "Cannot load image at: %s from request %s, file does not exist", image_file_path, request_id
            )
            return

        target_file_path = target_folder / original_file_path
        self.logger.debug("Moving sorted image to: %s", target_file_path)
        try:
            image_file_path.rename(target_file_path)
            self.logger.info("Moved file to %s for request %s", target_file_path, request_id)
        except FileExistsError:
            self.logger.error("File already exists, cannot sort")
        self.logger.info("Finished processing of request %s", request_id)
