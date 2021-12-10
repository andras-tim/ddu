FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN set -xe \
    && apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y \
        python3 \
        python3-pip \
    && apt-get clean

COPY requirements.txt /srv/
RUN set -xe \
    && python3 -m pip install -r /srv/requirements.txt

COPY ddu /srv/ddu

WORKDIR /srv
ENTRYPOINT ["python3", "-m", "ddu"]
