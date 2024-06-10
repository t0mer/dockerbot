FROM ubuntu:latest

LABEL maintainer="tomer.klein@gmail.com"
RUN apt update -yqq && \
    apt install -yqq python3-pip && \
    apt install -yqq curl && \
    apt install -yqq speedtest-cli && \
    apt install -yqq wget

ENV API_KEY ""

COPY requirements.txt /tmp

RUN pip3 install --upgrade pip setuptools --no-cache-dir

RUN pip3 install -r /tmp/requirements.txt

RUN wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/lib/python3/dist-packages/speedtest.py

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot



ENTRYPOINT ["/usr/bin/python3", "/opt/dockerbot/dockerbot.py"]
