from dataclasses import dataclass
from typing import Any


class ImageInputParsingError(Exception):
    pass


@dataclass
class ImageInputMessage:
    request_id: str
    file_path: str

    @classmethod
    def from_dict(cls, deserialized_message: dict[str, Any]) -> "ImageInputMessage":
        try:
            request_id: str = deserialized_message["request_id"]
            file_path: str = deserialized_message["file_path"]
        except KeyError as exc:
            raise ImageInputParsingError("Malformed message received") from exc
        return ImageInputMessage(request_id, file_path)

    def __post_init__(self) -> None:
        try:
            self.validate_request_id()
            self.validate_file_path()
        except AssertionError as exception:
            raise ImageInputParsingError("Could not validate message") from exception

    def validate_request_id(self) -> None:
        assert isinstance(self.request_id, str)

    def validate_file_path(self) -> None:
        assert isinstance(self.file_path, str)


@dataclass
class ImageSortedMessage:
    request_id: str
    mean_color: str
    file_path: str
