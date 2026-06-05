# Copyright 2026 PageKey Solutions, LLC

.PHONY: all build clean publish
all: build


# Variables.
DIST := dist
PACKAGE_NAME := hex
PACKAGE := dist/$(PACKAGE_NAME)
SRC := $(shell find . -type f -name '*.py')

# Targets.
$(DIST):
	mkdir -p $(DIST)

$(PACKAGE): $(DIST) pyproject.toml $(SRC) clean
	uv build
	uv run pyinstaller --onefile -n hex src/hex/main.py --hidden-import=requests


# Phony Targets.
build: $(PACKAGE)

clean:
	rm -rf $(DIST) *.egg-info
