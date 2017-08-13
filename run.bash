#!/bin/bash
# echo "start"


function start_virtualenv {
    . venv/bin/activate
}

function stop_virtualenv {
    deactivate
}

# Check arguments
if [[ $# -gt 0 ]]; then
    finished=0
    if [[ "$1" = "install" ]]; then
        echo "Will install packages"
        virtualenv venv
        start_virtualenv
        pip3 install colorama
        pip3 install pep8
        pip3 install autopep8
        pip3 install pytest
        pip3 install mock
        pip3 install parse
        pip3 install requests
        finished=1
    elif [[ "$1" = "autopep8" ]]; then
        echo "Will run autopep8"
        start_virtualenv
        autopep8 --in-place FantasyFootball/*.py FantasyFootball/parsers/*py
        finished=1
    fi

    if [[ $finished -eq 1 ]]; then
        stop_virtualenv
        exit
    fi
fi


start_virtualenv

#
# Unit tests
#
python -m pytest -q -x tests
rc=$?
if [ $rc -ne 0 ]; then
    echo "unit tests failed. rc=$rc"
    stop_virtualenv
    exit
fi


#
# Do some style checks
#
pep8 FantasyFootball/*.py FantasyFootball/parsers/*py
rc=$?
if [ $rc -ne 0 ]; then
    echo "style checks failed. rc=$rc"
    stop_virtualenv
    exit
fi


# Run the program
python main.py $@


# Clean up
stop_virtualenv
exit $rc
