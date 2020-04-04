#!/usr/bin/env bash

# Wrapper for starting the application
# This is file can safely be symlinked for easy use of the application

real_path="$(readlink "$0" || readlink -f "$0")"
DIRECTORY="$(dirname "$real_path")"

# shellcheck disable=SC1091
cd "$DIRECTORY" && source ./venv/bin/activate && python3 -m application.main "$@"
