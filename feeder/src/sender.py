import asyncio

from feeder.feeder import Feeder
from feeder.config import config

async def process_folder() -> None:
    app = Feeder(config)
    await app.start()
    await app.process_folder()

async def main() -> None:
    await process_folder()

if __name__ == "__main__":
    asyncio.run(main())
