#!/bin/sh

<<EOF
  This script is used to install the package from source for testing purposes.
EOF

# Find the python executable
python_executable=$(which python)
if [ -z "$python_executable" ]; then
    python_executable=$(which python3)
fi

rm -rf dist 

$python_executable -m pip install --upgrade build
$python_executable -m build

pip uninstall wpdetect -y
pip install dist/wpdetect-*-py3-none-any.whl