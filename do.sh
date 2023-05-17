#!/bin/bash

# The "do scripts" need to know the project root directory, in order
# to properly import each other. This directory is passed down as an
# environment variable.

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
export PYTHONPATH="${PYTHONPATH}:$PARENT_DIR"

python3 "$1.py"