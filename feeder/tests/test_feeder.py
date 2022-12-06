from unittest.mock import AsyncMock

import pytest

from feeder.feeder import Feeder

from .config import config


@pytest.fixture(name="feeder")
def fixture_feeder() -> Feeder:
    fixture = Feeder(config)
    fixture.producer = AsyncMock(name="producer")
    return fixture


class TestProcessFolder:
    @pytest.mark.asyncio
    async def test_folder(self, feeder: Feeder) -> None:
        feeder.process_file = AsyncMock(name="process_file")
        await feeder.process_folder()

        feeder.process_file.assert_awaited_with("white.png")
        feeder.process_file.assert_awaited_with("yellow.png")
