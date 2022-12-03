import os

config = {
    "consumer": {
        "username": "guest",
        "password": os.environ["RABBITMQ_IMAGESORT_PASSWORD"],
        #"hostname": os.environ["RABBITMQ_PROD_HOSTNAME"],
        "hostname": "localhost",
        "queue_name": "imagesort.sorted",
    },
    # "dump_folder": os.environ["IMAGESORT_DUMPER_FOLDER"],
    "dump_folder": "dump",
}
