FROM python:3.9.1-slim-buster

ENV POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./parser /code/parser
