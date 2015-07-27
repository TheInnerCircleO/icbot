#!/usr/bin/env bash
set -o errexit -o pipefail


## PRE-RUN SETUP & CONFIGURATION
########################################

## Set some paths
SCRIPT_DIR="$(dirname $(readlink -f ${0}))"
OUR_PLUGINS_DIR="${SCRIPT_DIR}/plugins"
BOT_PLUGINS_DIR="${SCRIPT_DIR}/hangupsbot/hangupsbot/plugins"

# Require python3
if [[ ! -x "$(which python3)" ]]; then
    echo "ERROR: python3 not found"; exit 1
fi


## SCRIPT USAGE
########################################

function usageShort() {
    echo "Usage: $(basename ${0}) [OPTIONS]"
}

function usageLong() {

    usageShort

	cat <<-EOF

	OPTIONS:

	    -c, --config    Config storage path
	    -h, --help      Print this help dialogue
	    -k, --cookies   Cookies storage path
	    -l, --log       Log file path
	    -m, --memory    Memory storage path

	Examples:

	    Run bot with a specific config file

	        ./run.sh --config path/to/config.json

	     Run bot with a specific memory and cookie files

	        ./run.sh --memory path/to/memory.json --cookies path/to/cookies.json
	EOF

}


## OPTION / PARAMATER PARSING
########################################

### Parse options with getopt
PARSED_OPTIONS=$(getopt -n "${0}" -o c:k:hl:m: -l "config:,cookies:,help,log:,memory:" -- "$@")

## Evaluate parsed options
eval set -- "${PARSED_OPTIONS}"

## Process script options
while true; do
    case "${1}" in

        -c|--config)

            shift

            ## Set config argument
            CONFIG_ARG="--config ${1}"; shift

        ;;

        -k|--cookies)

            shift

            ## Set cookie argument
            COOKIE_ARG="--cookies ${1}"; shift

        ;;

        -h|--help)

            ## Display usage info
            usageLong; exit

        ;;

        -l|--log)

            shift

            ## Set log argument
            LOG_ARG="--log ${1}"; shift

        ;;

        -m|--memory)

            shift

            ## Set memory argument
            MEMORY_ARG="--memory ${1}"; shift

        ;;

        --)

            ## Stop parsing options
            shift; break

        ;;

        *)

            ## This should never trigger, throw error if it does
            echo "ERROR: Internal error!"; exit 1

        ;;

    esac
done


## SCRIPT FUNCTIONS
########################################

function createSymlinks() {

    echo "Symlinking custom plugins to ${BOT_PLUGINS_DIR}:"

    ## SYMLINK ALL THE THINGS!!!
    for PLUGIN in ${OUR_PLUGINS_DIR}/*; do

        BASENAME="$(basename ${PLUGIN})"

        echo -n "  --> ${BASENAME}: "

        if [[ -h "${BOT_PLUGINS_DIR}/${BASENAME}" ]]; then
            echo "[OK] Symlink already exist"
        elif [[ -f "${BOT_PLUGINS_DIR}/${BASENAME}" ]]; then
            echo "[WARNING] Regular file with this name exists"
        else
            if [[ $(pushd ${BOT_PLUGINS_DIR} && ln -s ../../../plugins/${BASENAME} && popd) ]]; then
                echo "[NOTICE] Created symlink"
            else
                echo "[ERROR] Failed to create symlink"
            fi
        fi

    done

}


function runHangupsbot() {

    ## Run the hangupsbot
    python3 ${SCRIPT_DIR}/hangupsbot/hangupsbot/hangupsbot.py \
        ${CONFIG_ARG} \
        ${COOKIE_ARG} \
        ${LOG_ARG} \
        ${MEMORY_ARG}

}


function main() {

    ## Create plugin symlinks and run hangupsbot
    createSymlinks && runHangupsbot

}


## DO STUFF
########################################

main
