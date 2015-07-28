#!/usr/bin/env bash
set -o errexit -o pipefail


## PRE-RUN SETUP & CONFIGURATION
#######################################

# Require python3
if [[ ! -x "$(which python3)" ]]; then
    echo "ERROR: python3 not found"; exit 1
fi

SCRIPT_DIR="$(dirname $(readlink -f ${0}))"
VENV_DIR="${SCRIPT_DIR}/.venv-test"
COMMIT_HASH="$(git rev-parse --short HEAD)"
IMAGE_NAME="theinnercircle/icbot:test-${COMMIT_HASH}"



## SCRIPT USAGE
########################################

function usageShort() {
    echo "Usage: $(basename ${0}) [OPTIONS]"
}


function usageLong() {

    usageShort

	cat <<-EOF

	OPTIONS:

	    -h, --help     Print this help dialogue
	    -k, --keep     Don't delete the Docker image after run

	EOF

}


## OPTION / PARAMATER PARSING
########################################

while true; do
    case "${1}" in

        -h|--help)

            ## Display usage info
            usageLong; exit

        ;;

        -k|--keep)

            ## Set config argument
            KEEP="true"; shift

        ;;

        *)

            if [[ ! -z "${1}" ]]; then
                 usageLong; echo "ERROR: Unknown argument: ${1}";exit 1
            fi

            break

        ;;

    esac
done


## SCRIPT FUNCTIONS
########################################

function enable_venv() {

    # Create VENV_DIR if non-existant
    [[ -d "${VENV_DIR}" ]] || virtualenv -p $(which python3) ${VENV_DIR}

    # Load the virtual environment
    source ${VENV_DIR}/bin/activate

}


function disable_venv() {

    # Deactivate virtual environment
    if [[ ${TRAVIS} != "true" ]]; then
        deactivate
    fi

}


function install_dependencies() {

    # Install test dependencies
    pip3 install --upgrade tox -r ${SCRIPT_DIR}/test-requirements.txt

}


function docker_build() {

    docker build --force-rm --no-cache --pull --tag ${IMAGE_NAME} ${SCRIPT_DIR}

}


function docker_cleanup() {

    # Remove Docker image
    docker rmi -f ${IMAGE_NAME}

}


function cleanup() {

    docker_cleanup && disable_venv

}


function main() {

    # Set cleanup trap
    trap cleanup SIGKILL SIGTERM

    # Enable venv and install dependencies
    if [[ ${TRAVIS} != "true" ]]; then
        enable_venv && install_dependencies
    fi

    # Run tests
    tox && docker_build

    # Remove Docker images
    if [[ ${KEEP} != "true" ]]; then
        docker_cleanup
    fi

    disable_venv

}


## DO STUFF
########################################

main
