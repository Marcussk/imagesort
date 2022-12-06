from pathlib import Path

parent_directory: Path = Path(__file__).parent

config = {
    "consumer": {
        "username": "guest",
        "password": "guest",
        "hostname": "localhost",
        "queue_name": "imagesort.sorted",
    },
    "dump_folder": parent_directory / "images",
    "log_level": "DEBUG",
}
