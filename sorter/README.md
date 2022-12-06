# Sorter

Module that parses `ImageInputMessage`s from `imagesort.input` queue for requests to sort images and calculates `mean_color` that gets passed to dumper. 

## Development

This application uses Poetry for package dependendancies and configuration.

`poetry install`

Run pytest test

`poetry run pytest`

Code formatting

`poetry run poe format-code`
