import os

config = {
    "consumer": {
        "username": "guest",
        "password": os.environ["RABBITMQ_IMAGESORT_PASSWORD"],
        #"hostname": os.environ["RABBITMQ_PROD_HOSTNAME"],
        "hostname": "localhost",
        "queue_name": "imagesort.input",
    },
    "producer": {
        "username": "guest",
        "password": os.environ["RABBITMQ_IMAGESORT_PASSWORD"],
        #"hostname": os.environ["RABBITMQ_PROD_HOSTNAME"],
        "hostname": "localhost",
        "queue_name": "imagesort.sorted",
    },
}
