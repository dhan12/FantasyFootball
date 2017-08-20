#!/bin/bash
# Wrapper script to use while developing this application.

# Run given command and exit if it fails.
# arg 1-n: The command with parameters to run.
function run {
    cmd="${@:1}"
    eval $cmd
    rc=$?

    if [[ $rc -ne 0 ]]; then
        echo "Failed to run cmd: \"$cmd\", rc: $rc"
        clean_and_exit $rc
    fi
}

# Turn off virtual enviornment and exit.
# arg 1: Is the rcode to exit with.
function clean_and_exit {
    deactivate
    exit $1
}


if [[ "$1" = "install" ]]; then
	run virtualenv .venv
	run . .venv/bin/activate
	run pip3 install -r requirements.txt
	run pip3 install pep8 autopep8 pytest mock
else
    # Set up environment
    run . .venv/bin/activate
    run python setup.py -q develop

    # Test
    run autopep8 --in-place -r setup.py FantasyFootball tests
    run pep8 -r setup.py FantasyFootball tests
    run python -m pytest tests

    # Run and exit
    run FantasyFootball $@
fi

clean_and_exit 0
