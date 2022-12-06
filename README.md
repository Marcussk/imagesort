# imagesort

Application for sorting images on file system according to their mean color.

- `feeder` periodically accesses project folder and propagates files to system
- `sorter` calculates mean color for sorting
- `dumper` moves images to correct folder

## Usage

This project requires Docker and uses docker-compose to run individual components.

- `docker compose up` to start components
- move images to `images` folder, or alternatively update `IMAGESORT_DUMPER_FOLDER` in compose for using any folder
- review sorted image

## Local development

For local development python3.11 and poetry is needed.
Individual components expect these envs to work:

- IMAGESORT_FOLDER
- RABBITMQ_HOSTNAME
- RABBITMQ_USERNAME
- RABBITMQ_PASSWORD

Additional optional envs that configure behavior:

- IMAGESORT_FEEDER_LOG_LEVEL
- IMAGESORT_SORTER_LOG_LEVEL
- IMAGESORT_DUMPER_LOG_LEVEL
- IMAGESORT_FEEDER_BACKOFF