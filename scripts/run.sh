#!/bin/bash
if [ $1 == "server" ]; then
    exec python poucave

elif [ $1 == "check" ]; then
    shift
    exec python poucave $@

elif [ $1 == "test" ]; then
    if [ $EUID != 0 ]; then
        echo "Need to be root.  Run container with '--user root'"
        exit 1
    fi

    pip install --progress-bar=off -r requirements/dev.txt
    pytest tests

else
    exec "$@"
fi