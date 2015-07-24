#!/usr/bin/env bash
set -o errexit -o pipefail


## PRE-RUN SETUP & CONFIGURATION
#######################################

SCRIPT_DIR="$(dirname $(readlink -f ${0}))"
VENV_DIR="${SCRIPT_DIR}/.venv-test"

# Require python3
if [[ ! -x "$(which python3)" ]]; then
    echo "ERROR: python3 not found"; exit 1
fi


## SCRIPT FUNCTIONS
########################################

function enable_venv() {

    # Create VENV_DIR if non-existant
    [[ -d "${VENV_DIR}" ]] || virtualenv -p $(which python3) ${VENV_DIR}

    # Load the virtual environment
    source ${VENV_DIR}/bin/activate

}

function install_dependencies() {

    # Install bot dependencies
    pip3 install --upgrade -r ${SCRIPT_DIR}/requirements.txt -r ${SCRIPT_DIR}/hangupsbot/requirements.txt

    # Install test dependencies
    pip3 install --upgrade tox -r ${SCRIPT_DIR}/test-requirements.txt

}


function run_tests() {

    tox

    docker build --force-rm --no-cache --pull --tag theinnercircle/icbot:test ${SCRIPT_DIR}

}

function cleanup() {

    # Remove docker image
    docker rmi -f theinnercircle/icbot:test

    # Deactivate virtual environment
    deactivate

}


function main() {

    # Set cleanup trap
    trap cleanup EXIT SIGKILL SIGTERM

    if [[ ${TRAVIS} != "true" ]]; then

        # Enable venv and install dependencies
        enable_venv && install_dependencies

    fi

    # Run tests
    run_tests

}


## DO STUFF
########################################

main
