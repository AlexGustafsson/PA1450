# Disable echoing of commands
MAKEFLAGS += --silent

# Ensure that Bash is used as the default shell
SHELL := /usr/bin/env bash

# The Python binary to use. Expects Python 3.8 available as python3. Use the
# PYTHON environment variable to change it. Do not change it here
PYTHON ?= python3.8
python := $(PYTHON)

# The main module of the project
main_module := application

# Paths to all source files
source := $(shell find $(main_module) -name '*.py' -not -name '__init__.py')

# Install necessary components
install: install-virtual-environment install-dependencies

# Install the virtual environment
install-virtual-environment:
	$(python) -m venv venv

# Install all dependencies listed in requirements.txt
install-dependencies:
	source venv/bin/activate && $(python) -m pip install -r requirements.txt

# Clean all dynamically created files
clean:
	rm -rf venv data > /dev/null 2>&1 || :
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
