from dataclasses import asdict

import pytest

from dumper.models import ImageSortedMessage, ImageSortedParsingError

serialized_message = {
    "request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8",
    "mean_color": "#ffffff",
    "file_path": "white.png",
}


class TestImageSorted:
    def test_init(self) -> None:
        model = ImageSortedMessage(
            request_id="679f6fa9-ced2-4ecd-9d18-664908ebd6f8", mean_color="#ffffff", file_path="white.png"
        )
        assert model == ImageSortedMessage.from_dict(serialized_message)
        assert asdict(model) == serialized_message

    def test_missing_fields(self) -> None:
        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict({})

        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict(
                {"request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8", "mean_color": "#ffffff"}
            )

        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict(
                {"request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8", "file_path": "white.png"}
            )

        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict({"file_path": "white.png", "mean_color": "#ffffff"})

    def test_correct_datatypes(self) -> None:
        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict({"request_id": 0, "mean_color": "#ffffff", "file_path": "white.png"})

        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict(
                {"request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8", "mean_color": 0.0, "file_path": False}
            )

        with pytest.raises(ImageSortedParsingError):
            ImageSortedMessage.from_dict(
                {"request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8", "mean_color": "#ffffff", "file_path": False}
            )
