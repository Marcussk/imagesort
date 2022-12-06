FROM python:3.11 as python-base

RUN pip install poetry
WORKDIR /build

# dependancies for opencv
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

FROM python-base as builder

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt
RUN poetry build

FROM python-base

# install app dependancies only
COPY --from=builder /build/requirements.txt .
RUN pip install -r requirements.txt

# install app
COPY --from=builder /build/dist dist
RUN pip install --no-deps dist/*.whl

WORKDIR /usr/src/app

CMD ["python", "-m", "sorter"]
