import asyncio

from .config import config
from .sorter import Sorter

async def run() -> None:
    try:
        print("Initializing sorter")
        sorter = Sorter(config)
        print("Starting sorter")
        await sorter.start()
        print("Running sorter")
        await sorter.run()
    except KeyboardInterrupt:
        pass

def main() -> None:
    print("Running application")
    asyncio.run(run())


if __name__ == "__main__":
    main()