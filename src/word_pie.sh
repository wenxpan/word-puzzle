#!/bin/bash
pyv="$(python3 -V 2>&1)"
if [[ $pyv == "Python 3"* ]]
then
    if [ $1 == "play" ] || [ $1 == "settings" ]
    then
        python3 -m venv .venv
        source .venv/bin/activate
        python3 -m pip install -r requirements.txt
        python3 main.py $1
        deactivate
    else
        echo "Invalid command. Please enter 'play' or 'settings' after ./wrapper.sh"
    fi
else
    echo "You need Python 3.10 or higher to run this application. You can download the latest version of Python at https://www.python.org/downloads/" >&2
fi