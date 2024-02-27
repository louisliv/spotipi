#!/bin/bash

# Ensure the virtual environment is activated
source env/bin/activate

# Run python setup.py sdist bdist_wheel
python setup.py sdist bdist_wheel

exit 0
