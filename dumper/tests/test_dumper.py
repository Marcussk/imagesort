from unittest.mock import AsyncMock, Mock

import pytest

from dumper.dumper import Dumper
from dumper.models import ImageSortedMessage

from .config import config


@pytest.fixture(name="dumper")
def fixture_dumper() -> Dumper:
    fixture = Dumper(config)
    fixture.consumer = AsyncMock(name="consumer")
    return fixture


class TestProcess:
    @pytest.mark.asyncio
    async def test_simple(self, dumper: Dumper) -> None:
        model = ImageSortedMessage(
            request_id="679f6fa9-ced2-4ecd-9d18-664908ebd6f8", mean_color="#ffffff", file_path="white.png"
        )
        dumper.dump_file = Mock(name="dump_file")

        await dumper.process(model)

        dumper.dump_file.assert_called_once_with("white.png", "white", "679f6fa9-ced2-4ecd-9d18-664908ebd6f8")


class TestGetColorName:
    def test_white(self, dumper: Dumper) -> None:
        assert dumper.get_color_name("#ffffff") == "white"

    def test_other(self, dumper: Dumper) -> None:
        """
        When color has no name, its value is used without # prefix
        """
        assert dumper.get_color_name("#6f6f6f") == "6f6f6f"
