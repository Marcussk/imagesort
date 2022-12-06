from dataclasses import asdict

import pytest

from sorter.models import ImageInputMessage, ImageInputParsingError


class TestImageInput:
    def test_init(self) -> None:
        model = ImageInputMessage(request_id="XXX", file_path="white.png")
        assert model == ImageInputMessage.from_dict(asdict(model))
        assert asdict(model) == {"request_id": "XXX", "file_path": "white.png"}

    def test_missing_fields(self) -> None:
        with pytest.raises(ImageInputParsingError):
            ImageInputMessage.from_dict({})

        with pytest.raises(ImageInputParsingError):
            ImageInputMessage.from_dict({"request_id": "XXX"})

        with pytest.raises(ImageInputParsingError):
            ImageInputMessage.from_dict({"file_path": "white.png"})

    def test_correct_datatypes(self) -> None:
        with pytest.raises(ImageInputParsingError):
            ImageInputMessage.from_dict({"request_id": 0, "file_path": "white.png"})

        with pytest.raises(ImageInputParsingError):
            ImageInputMessage.from_dict({"request_id": "XXX", "file_path": False})
