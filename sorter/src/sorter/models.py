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
            # TODO: test correct parsing, raises exceptions?
            request_id: str = deserialized_message["request_id"]
            file_path: str = deserialized_message["file_path"]
        except KeyError as exc:
            raise ImageInputParsingError("Malformed message received") from exc
        return ImageInputMessage(request_id, file_path)

# TODO: dataclass json?
@dataclass
class ImageSortedMessage:
    request_id: str
    mean_color: str