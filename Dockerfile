FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

ENV BOT_NAME=simple_bot

WORKDIR /usr/src/app/${BOT_NAME}

COPY requirements.txt /usr/src/app/${BOT_NAME}
RUN pip install -r /usr/src/app/${BOT_NAME}/requirements.txt
COPY . /usr/src/app/${BOT_NAME}
