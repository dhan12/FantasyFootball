#!/bin/bash


function clean_and_exit {
    deactivate
    echo $1
}

if [[ "$1" = "install" ]]; then
	virtualenv .venv
	. .venv/bin/activate
	pip3 install -r requirements.txt
	pip3 install pep8 autopep8 pytest mock
    exit 0
fi

# Set up environment
. .venv/bin/activate
python setup.py -q develop

# Test
autopep8 --in-place -r setup.py FantasyFootball tests
pep8 -r setup.py FantasyFootball tests || clean_and_exit 2
python -m pytest tests || clean_and_exit 3

# Run and exit
FantasyFootball $@
clean_and_exit 0
