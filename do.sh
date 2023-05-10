#!/bin/bash

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
export PYTHONPATH="${PYTHONPATH}:$PARENT_DIR"
python3 "$1.py"