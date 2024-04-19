FROM python:3.10-slim as builder

WORKDIR /tmp

RUN pip install pipenv

COPY ./Pipfile ./Pipfile.lock /tmp/

RUN pipenv requirements > requirements.txt

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/backend

COPY --from=builder /tmp/requirements.txt /usr/backend/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/backend/
