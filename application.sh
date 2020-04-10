#!/usr/bin/env bash

# Wrapper for starting the application
# This is file can safely be symlinked for easy use of the application

# The Python binary to use. Expects Python 3.8 available as python3. Use the
# PYTHON environment variable to change it. Do not change it here
PYTHON="${PYTHON:-python3.8}"
python="$PYTHON"

real_path="$(readlink "$0" || readlink -f "$0")"
DIRECTORY="$(dirname "$real_path")"

# shellcheck disable=SC1091
cd "$DIRECTORY" && source ./venv/bin/activate && "$python" -m application.main "$@"
