import asyncio
import time

from .config import config
from .feeder import Feeder


async def run() -> None:
    try:
        sorter = Feeder(config)
        print("Waiting on dependancies")
        time.sleep(10)
        await sorter.start()
        await sorter.run()
    except KeyboardInterrupt:
        pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
