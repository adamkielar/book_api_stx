FROM python:3.8-slim-buster
LABEL maintainer="Adam Kielar"

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get install -y --no-install-recommends libnss-wrapper && \
	rm -rf /var/lib/apt/lists/* && \
    apt-get clean

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /app && chmod -R 755 /app

## install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

USER user
COPY ./app /app