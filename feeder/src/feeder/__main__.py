import asyncio
import time

from .config import config
from .feeder import Feeder


async def run() -> None:
    try:
        feeder = Feeder(config)
        print("Waiting on dependancies")
        time.sleep(10)
        await feeder.start()
        await feeder.run()
    except KeyboardInterrupt:
        pass
    finally:
        await feeder.stop()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
