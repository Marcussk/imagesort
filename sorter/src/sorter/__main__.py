import asyncio
import time

from .config import config
from .sorter import Sorter


async def run() -> None:
    try:
        sorter = Sorter(config)
        print("Waiting on dependancies")
        time.sleep(1)
        await sorter.start()
        await sorter.run()
    except KeyboardInterrupt:
        pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
