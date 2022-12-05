from dataclasses import dataclass
from typing import Any


class ImageInputParsingError(Exception):
    pass


@dataclass
class ImageInputMessage:
    request_id: str
    file_path: str

    @classmethod
    def from_json(cls, deserialized_message: dict[str, Any]) -> "ImageInputMessage":
        try:
            request_id: str = deserialized_message["request_id"]
            file_path: str = deserialized_message["file_path"]
        except KeyError as exc:
            raise ImageInputParsingError("Malformed message received") from exc
        return ImageInputMessage(request_id, file_path)


@dataclass
class ImageSortedMessage:
    request_id: str
    mean_color: str
    file_path: str
