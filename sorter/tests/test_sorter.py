from unittest.mock import AsyncMock, Mock

import pytest

from sorter.models import ImageInputMessage, ImageSortedMessage
from sorter.sorter import Sorter

from .config import config


@pytest.fixture(name="sorter")
def fixture_sorter() -> Sorter:
    fixture = Sorter(config)
    fixture.producer = AsyncMock(name="producer")
    fixture.consumer = AsyncMock(name="consumer")
    return fixture


@pytest.mark.asyncio
async def test_process_image(sorter: Sorter) -> None:
    input_message = ImageInputMessage(request_id="XXX", file_path="white.png")
    sorted_message = ImageSortedMessage(request_id="XXX", mean_color="#ffffff", file_path="white.png")
    sorter.get_mean_color = Mock(name="get_mean_color", return_value="#ffffff")
    sorter.producer.send = AsyncMock(name="producer.send")

    await sorter.process_image(input_message)

    sorter.get_mean_color.assert_called_once_with(sorter.dump_folder / "white.png")
    sorter.producer.assert_awaited_once_with(sorted_message)


def test_get_mean_color(sorter: Sorter) -> None:
    test_image_path = str(sorter.dump_folder / "white.png")

    assert sorter.get_mean_color(test_image_path) == "#ffffff"
