FROM python:latest

LABEL maintainer="tomer.klein@gmail.com"

RUN pip3 install docker telepot  speedtest-cli --no-cache-dir

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENV API_KEY ""

ENTRYPOINT ["/usr/bin/python3", "/opt/dockerbot/dockerbot.py"]
