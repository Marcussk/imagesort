from dumper.models import ImageSortedMessage

serialized_message = {
    "request_id": "679f6fa9-ced2-4ecd-9d18-664908ebd6f8",
    "mean_color": "#ffffff",
    "file_path": "white.png",
}


def test_from_json():
    message = ImageSortedMessage(
        request_id="679f6fa9-ced2-4ecd-9d18-664908ebd6f8", mean_color="#ffffff", file_path="white.png"
    )
    assert message == ImageSortedMessage.from_json(serialized_message)
