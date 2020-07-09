FROM python:latest

LABEL maintainer="tomer.klein@gmail.com"

RUN pip install docker speedtest-cli --no-cache-dir
RUN pip install telepot

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENV API_KEY ""

ENTRYPOINT ["/usr/bin/python", "/opt/dockerbot/dockerbot.py"]
