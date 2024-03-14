#!/bin/bash

# Ensure the virtual environment is activated
source env/bin/activate

# Ensure dist directory is clean
rm -rf dist/*

# Run python setup.py sdist bdist_wheel
python src/setup.py sdist bdist_wheel

exit 0
