import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger()


class ImageSortedParsingError(Exception):
    pass


@dataclass
class ImageSortedMessage:
    request_id: str
    mean_color: str
    file_path: str

    @classmethod
    def from_json(cls, deserialized_message: dict[str, Any]) -> "ImageSortedMessage":
        try:
            request_id: str = deserialized_message["request_id"]
            mean_color: str = deserialized_message["mean_color"]
            file_path: str = deserialized_message["file_path"]
        except KeyError as exception:
            logger.exception("Missing field in message")
            raise ImageSortedParsingError("Malformed message received") from exception
        return ImageSortedMessage(request_id, mean_color, file_path)

    """
    def __post_init__(self) -> None:
        try:
            self.validate_request_id()
            self.validate_mean_color()
        except AssertionError as exception:
            raise ImageSortedParsingError("Could not validate message") from exception
    """

    def validate_request_id(self) -> None:
        assert isinstance(self.request_id, str)

    def validate_mean_color(self) -> None:
        assert isinstance(self.mean_color, str)
