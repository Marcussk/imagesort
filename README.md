# imagesort

Application for sorting images on file system according to their mean color.

- `sorter` calculates mean color for sorting
- `dumper` moves images to correct folder
- `extras\imagesort_sender.py` sends sorting request

## Usage

This project requires Docker and uses docker-compose to run individual components.

- `docker compose up` to start components
- move images to `images` folder, or alternatively update `IMAGESORT_DUMPER_FOLDER` in compose for using any folder
- send request for sorting to `imagesort.input` by using `imagesort_sender`.
- review sorted image

## Local development

For local development python3.11 and poetry is needed.
Individual components expect these envs to work:

- IMAGESORT_DUMPER_FOLDER
- RABBITMQ_HOSTNAME
- RABBITMQ_USERNAME
- RABBITMQ_PASSWORD
