FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"
RUN apt update -yqq && \
    apt install -yqq python-pip && \
    apt install -yqq curl && \
    apt install -yqq speedtest-cli && \
    apt install -yqq wget

COPY requirements.txt /tmp

RUN pip install --upgrade pip setuptools --no-cache-dir

RUN pip install -r /tmp/requirements.txt

RUN wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/lib/python3/dist-packages/speedtest.py

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENV API_KEY ""

ENTRYPOINT ["/usr/bin/python", "/opt/dockerbot/dockerbot.py"]
