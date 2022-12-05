# Sorter

Module that parses `ImageInputMessage`s from `imagesort.input` queue for requests to sort images. Input image is loaded and its mean color is calculated. Information about image is propagated to dumper by sending `ImageSortedMessage` to `imagesort.dump` queue.

## Development

This application uses Poetry for package dependendancies and configuration.

`poetry install`

Run pytest test

`poetry run pytest`

Code formatting

`poetry run poe format-code`
