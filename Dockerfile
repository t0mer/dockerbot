FROM python:latest

LABEL maintainer="tomer.klein@gmail.com"

RUN pip3 install docker telepot  --no-cache-dir

RUN mkdir /opt/dockerbot

RUN curl ipinfo.io/ip
