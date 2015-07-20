FROM ubuntu:14.04
MAINTAINER The Inner Circle <https://github.com/TheInnerCircleO>

## Set directory vars
ENV BOT_DIR /srv/icbot

## Upgrade packages and install dependencies
RUN apt-get update && apt-get -y upgrade \
    && apt-get -y install git python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

## Copy files to image
COPY ./ ${BOT_DIR}/

## Install bot dependencies
RUN pip3 install --upgrade -r ${BOT_DIR}/requirements.txt -r ${BOT_DIR}/hangupsbot/requirements.txt

## Create config volume
VOLUME ${BOT_DIR}/config

## Default command
CMD ${BOT_DIR}/run.sh \
    --config ${BOT_DIR}/config/config.json \
    --cookies ${BOT_DIR}/config/cookies.json \
    --log ${BOT_DIR}/config/hangupsbot.log \
    --memory ${BOT_DIR}/config/memory.json
