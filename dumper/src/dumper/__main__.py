import asyncio
import time

from .config import config
from .dumper import Dumper


async def run() -> None:
    try:
        dumper = Dumper(config)
        print("Waiting on dependancies")
        time.sleep(10)
        await dumper.start()
        await dumper.run()
    except KeyboardInterrupt:
        pass


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
