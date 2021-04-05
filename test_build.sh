#!/bin/bash

# Usage: ./test_build.sh [2|3]
# Builds package and tests wheel

python3 setup.py sdist bdist_wheel

export DJANGO_SETTINGS_MODULE='tests.settings'
TEST="tests"
echo $TEST

FILE=`ls -1 dist/*.whl | tail -n 1`
echo "Verifying build of $FILE"

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
