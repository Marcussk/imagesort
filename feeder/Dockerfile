FROM python:3.11 as python-base

RUN pip install poetry
WORKDIR /build

FROM python-base as builder

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt
RUN poetry build

FROM python-base

COPY --from=builder /build/requirements.txt .
RUN pip install -r requirements.txt

COPY --from=builder /build/dist dist
RUN pip install --no-deps dist/*.whl

WORKDIR /usr/src/app

CMD ["python", "-m", "dumper"]
