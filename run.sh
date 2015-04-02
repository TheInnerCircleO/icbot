#!/usr/bin/env bash
set -o errexit -o pipefail

## Set some paths
SCRIPT_PATH="$(dirname $(readlink -f ${0}))"
OUR_PLUGINS_DIR="${SCRIPT_PATH}/plugins"
BOT_PLUGINS_DIR="${SCRIPT_PATH}/hangupsbot/hangupsbot/plugins"

## SYMLINK ALL THE THINGS!!!
for PLUGIN in ${OUR_PLUGINS_DIR}/*; do

    BASENAME="$(basename ${PLUGIN})"

    if [[ ! -h "${BOT_PLUGINS_DIR}/${BASENAME}" ]]; then
        ln -s ${PLUGIN} ${BOT_PLUGINS_DIR}/${BASENAME}
    fi

done

## Run the bot
python3 ${SCRIPT_PATH}/hangupsbot/hangupsbot/hangupsbot.py --config ${SCRIPT_PATH}/icbot-config.json
