import os

config = {
    "consumer": {
        "username": "guest",
        "password": "guest",
        #"password": os.environ["RABBITMQ_PASSWORD"],
        "hostname": os.environ["RABBITMQ_HOSTNAME"],
        #"hostname": "localhost",
        "queue_name": "imagesort.input",
    },
    "producer": {
        "username": "guest",
        "password": "guest",
        #"password": os.environ["RABBITMQ_PASSWORD"],
        "hostname": os.environ["RABBITMQ_HOSTNAME"],
        #"hostname": "localhost",
        "queue_name": "imagesort.sorted",
    },
    "dump_folder": os.environ["IMAGESORT_DUMPER_FOLDER"],
}
