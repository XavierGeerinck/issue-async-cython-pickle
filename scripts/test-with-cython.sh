#!/bin/bash -e
#
# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
#
################################################################################
## File:    test-with-cython.sh
## Desc:    Runs the provided file or directory with Cython enabled
## Usage:   test-with-cython.sh <FILE_OR_DIR>
## Example: ./test-with-cython.sh my_module/tests/test_async_cython.py
################################################################################

# Variables
FILE=$1

# Process the FILE or DIR argument, we split on / and the first segment is the directory
MODULE_PATH=$(echo "$FILE" | cut -d'/' -f1)

# If packages already installed
if [[ $(pip list | grep my_module) ]]; then
    echo "Removing test packages"
    pip uninstall -y my_module > /dev/null
fi

# Install Packages
echo "Compiling modules to Cython"

echo "- my_module"
cd my_module
CIBUILDWHEEL="1" python -m pip install -e . > /dev/null

cd ../

# Run tests
MODULE_PATH_TEST=${FILE/$MODULE_PATH\//}
echo "Running tests for '${MODULE_PATH}' (path: ${MODULE_PATH_TEST})"
cd $MODULE_PATH
python -m pytest -vs $MODULE_PATH_TEST
cd ..
