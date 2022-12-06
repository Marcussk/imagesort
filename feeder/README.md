# Feeder

Module that periodically checks input folder given by env `IMAGESORT_FOLDER` and feeds any files in that folder to sorter for processing.

Script `sender.py` is provided to enable one time processing of image folder.

## Development

This application uses Poetry for package dependendancies and configuration.

`poetry install`

Run pytest test

`poetry run pytest`

Code formatting

`poetry run poe format-code`
