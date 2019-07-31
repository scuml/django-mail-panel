#!/bin/bash

# Usage: ./test_build.sh [2|3]
# Builds package and tests wheel in python 2 and 3
# Add 2 or 3 to test a particular version of python

python3 setup.py sdist bdist_wheel

export DJANGO_SETTINGS_MODULE='tests.settings'
TEST="tests"
echo $TEST

FILE=`ls -1 dist/*.whl | tail -n 1`
echo "Verifying build of $FILE"

if [ -z "$1" ] || [ "$1" -eq "2" ]; then
    echo "# Installing virtualenv for Python 2"
    rm -rf 27-sdist  # ensure clean state if ran repeatedly
    virtualenv 27-sdist

    echo "# Install Python 2 requirements"
    27-sdist/bin/pip install django $FILE

    echo "# Run command with Python 2"
    27-sdist/bin/python -m "$TEST"

    echo "# Test using Python 2 ended"
fi

if [ -z "$1" ] || [ "$1" -eq "3" ]; then
    echo "# Installing virtualenv for Python 3"
    rm -rf 3-sdist  # ensure clean state if ran repeatedly
    virtualenv -p python3 3-sdist

    echo "# Install Python 3 requirements"
    3-sdist/bin/pip3 install django $FILE

    echo "# Run command with Python 3"
    3-sdist/bin/python3 -m "$TEST"

    echo "# Test using Python 3 ended"
fi
