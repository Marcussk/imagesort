from feeder.models import ImageInputMessage


class TestImageInput:
    def test_init(self) -> None:
        model = ImageInputMessage.from_file_path("white.png")
        assert isinstance(model.request_id, str)
        assert model.file_path == "white.png"
