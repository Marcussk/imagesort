import asyncio

from .config import config
from .dumper import Dumper

async def main():
    dumper = Dumper(config)
    await dumper.start()
    await dumper.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyError:
        pass
