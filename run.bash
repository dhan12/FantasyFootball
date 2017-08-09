#!/bin/bash
echo "start"


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
        pip install colorama
        pip install pep8
        pip install autopep8
        pip install pytest
        pip install mock
        pip install parse
        finished=1
    elif [[ "$1" = "autopep8" ]]; then
        echo "Will run autopep8"
        start_virtualenv
        autopep8 --in-place *.py src/parsers/*py
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
python -m pytest -x tests
rc=$?
if [ $rc -ne 0 ]; then
    echo "unit tests failed. rc=$rc"
    stop_virtualenv
    exit
fi


#
# Do some style checks
#
pep8 *.py src/parsers/*.py
rc=$?
if [ $rc -ne 0 ]; then
    echo "style checks failed. rc=$rc"
    stop_virtualenv
    exit
fi


# Run the program
python process.py $@


# Clean up
stop_virtualenv
exit $rc
