#!/usr/bin/env bash
set -o errexit -o pipefail


## PRE-RUN SETUP & CONFIGURATION
########################################

## Set some paths
SCRIPT_DIR="$(dirname $(readlink -f ${0}))"
OUR_PLUGINS_DIR="${SCRIPT_DIR}/plugins"
BOT_PLUGINS_DIR="${SCRIPT_DIR}/hangupsbot/hangupsbot/plugins"


## SCRIPT USAGE
########################################

function usageShort() {
    echo "Usage: $(basename ${0}) [OPTIONS]"
}

function usageLong() {

    usageShort

	cat <<-EOF

	OPTIONS:

	    -c, --config    Path to config file
	    -h, --help      Print this help dialogue

	Examples:

	    Run bot with a specific config file

	        ./run.sh --config path/to/config.json
	EOF

}


## OPTION / PARAMATER PARSING
########################################

### Parse options with getopt
PARSED_OPTIONS=$(getopt -n "${0}" -o c:h -l "config:,help" -- "$@")

## Evaluate parsed options
eval set -- "${PARSED_OPTIONS}"

## Process script options
while true; do
    case "${1}" in

        -c|--config)

            shift

            ## Set config argument
            if [[ -r ${1} ]]; then
                CONFIG_ARG="--config ${1}"; shift
            else
                echo "ERROR: Config file does not exist "; exit 1
            fi

        ;;

        -h|--help)

            ## Display usage info
            usageLong; exit

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
            if $(ln -s ${PLUGIN} ${BOT_PLUGINS_DIR}/${BASENAME}); then
                echo "[NOTICE] Created symlink"
            else
                echo "[ERROR] Failed to create symlink"
            fi
        fi

    done

    if [[ -z "${CONFIG_PATH}" ]]; then
        CONFIG_PATH="${HOME}/.local/share/hangupsbot/config.json"
    fi

}


function runHangupsbot() {

    ## Run the hangupsbot
    python3 ${SCRIPT_DIR}/hangupsbot/hangupsbot/hangupsbot.py ${CONFIG_ARG}

}


function main() {

    ## Create plugin symlinks and run hangupsbot
    createSymlinks && runHangupsbot

}


## DO STUFF
########################################

main
