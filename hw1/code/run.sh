#!/bin/sh
if [ "$#" -eq 3 ]; then
python3 sbp.py "$1" "$2" "$3"
elif [ "$#" -eq 2 ]; then
python3 sbp.py "$1" "$2"
elif [ "$#" -eq 1 ]; then
python3 sbp.py "$1"
else
echo "Usage: ./run.sh <command> [<optional-argument>]"
fi
