from dataclasses import dataclass
from datetime import datetime
from typing import Any

from aio_pika.abc import AbstractIncomingMessage


class MessageParsingException(Exception):
    pass


@dataclass
class ImageSortedMessage:
    inserted_timestamp: datetime
    request_id: str
    mean_color: str

    @classmethod
    def from_json(cls, deserialized_message: dict[str, Any]) -> "ImageSortedMessage":
        try:
            # TODO: test correct parsing, raises exceptions?
            inserted_timestamp: datetime = datetime.fromisoformat(deserialized_message["inserted_timestamp"])
            request_id: str = deserialized_message["request_id"]
            mean_color: str = deserialized_message["sort_key"]
        except KeyError as exc:
            raise MessageParsingException("Malformed message received") from exc
        return ImageSortedMessage(inserted_timestamp, request_id, mean_color)

    def __post_init__(self) -> None:
        try:
            self.validate_inserted_timestamp()
            self.validate_request_id()
            self.validate_mean_color()
        except AssertionError as exception:
            raise MessageParsingException("Could not validate message") from exception

    def validate_inserted_timestamp(self) -> None:
        assert isinstance(self.inserted_timestamp, datetime)

    def validate_request_id(self) -> None:
        assert isinstance(self.request_id, str)

    def validate_mean_color(self) -> None:
        assert isinstance(self.mean_color, str)
