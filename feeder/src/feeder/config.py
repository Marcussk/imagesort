import os

config = {
    "producer": {
        "username": "guest",
        "password": "guest",
        "hostname": os.environ["RABBITMQ_HOSTNAME"],
        "queue_name": "imagesort.input",
    },
    "dump_folder": os.environ["IMAGESORT_DUMPER_FOLDER"],
    "log_level": os.environ.get("IMAGESORT_SORTER_LOG_LEVEL", "INFO"),
    "backoff_time": os.environ.get("IMAGESORT_FEEDER_BACKOFF", 10)
}
