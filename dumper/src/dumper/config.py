import os

config = {
    "consumer": {
        "username": "guest",
        "password": "guest",
        "hostname": os.environ["RABBITMQ_HOSTNAME"],
        "queue_name": "imagesort.sorted",
    },
    "dump_folder": os.environ["IMAGESORT_FOLDER"],
    "log_level": os.environ.get("IMAGESORT_DUMPER_LOG_LEVEL", "INFO")
}
