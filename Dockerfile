FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"
RUN apt update
RUN apt install python3-pip --yes
RUN pip3 install docker speedtest-cli --no-cache-dir
RUN pip3 install telepot

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENV API_KEY ""

ENTRYPOINT ["/usr/bin/python3", "/opt/dockerbot/dockerbot.py"]
