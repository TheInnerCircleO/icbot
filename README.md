icbot
=====

**!!! DEPRECATED !!!** - This project has moved to <https://github.com/TheInnerCircleO/docker-icbot>.

-----

Chat bot for The Inner Circle Google Hangouts chat.

[![Build Status](https://travis-ci.org/TheInnerCircleO/icbot.svg?branch=master)](https://travis-ci.org/TheInnerCircleO/icbot)

### Cloning the bot + submodules

    git clone --recursive git@github.com:TheInnerCircleO/icbot.git


### Prerequisites

Install prerequisites:

    sudo apt-get install git python3 python3-pip python-virtualenv


### Installing requirements

First cd to the project's root dir:

    cd path/to/icbot


Set up and activate your virtual environment:

    virtualenv -p /usr/bin/python3 .venv
    source .venv/bin/activate


Install requirements:

    pip3 install --upgrade -r requirements.txt -r hangupsbot/requirements.txt


Install testing requirements (optional):

    pip3 install --upgrade tox -r test-requirements.txt


### Running the bot

Run the bot with defaults:

    ./run.sh

Usage:

    Usage: run.sh [OPTIONS]

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


### Docker

**Build a Docker image**

You can build an image locally for testing or running a bot. From the icbot
directory run the following:

    docker build --force-rm --pull --tag theinnercircle/icbot .

**First run & authentication**

The first time you run the bot you have to authenticate it manually.  To do
this run the bot interactively and follow the instructions given:

    docker run -it --rm -v /local/config/dir:/srv/icbot/config theinnercircle/icbot

**Running from Docker**

Once authenticated you can use `Ctrl + C` to kill the running container and run
a daemonized instance of the bot image:

    docker daemon -t -v /local/config/dir:/srv/icbot/config --restart=always --name icbot theinnercircle/icbot

-----

**Copyright (c) 2015 The Inner Circle <https://github.com/TheInnerCircleO>**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
