FROM python:latest

LABEL maintainer="tomer.klein@gmail.com"

RUN pip install docker telepot  speedtest-cli --no-cache-dir

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENV API_KEY ""

ENTRYPOINT ["/usr/bin/python", "/opt/dockerbot/dockerbot.py"]
