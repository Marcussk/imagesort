from dataclasses import dataclass
from uuid import uuid4


@dataclass
class ImageInputMessage:
    request_id: str
    file_path: str

    @classmethod
    def from_file_path(cls, file_path: str) -> "ImageInputMessage":
        return ImageInputMessage(request_id=str(uuid4()), file_path=file_path)
