import asyncio

from .config import config
from .dumper import Dumper

import time

async def run() -> None:
    try:
        print("Initializing dumper")
        dumper = Dumper(config)
        print("Waiting on dependancies")
        time.sleep(1)
        print("Starting dumper")
        await dumper.start()
        print("Running dumper")
        await dumper.run()
    except KeyboardInterrupt:
        pass

def main() -> None:
    print("Running application")
    asyncio.run(run())


if __name__ == "__main__":
    main()