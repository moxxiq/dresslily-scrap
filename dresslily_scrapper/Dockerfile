FROM python:3.9.6-slim-buster

WORKDIR /scrapper

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  pip install --upgrade pip && \
  apt install --no-install-recommends gcc -y && \
  rm -rf /var/lib/apt/lists/*
COPY requirements.txt /scrapper/
RUN pip install -r requirements.txt
COPY ./* /scrapper/
