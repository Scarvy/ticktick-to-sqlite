# ticktick-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/ticktick-to-sqlite.svg)](https://pypi.org/project/ticktick-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/Scarvy/ticktick-to-sqlite?include_prereleases&label=changelog)](https://github.com/Scarvy/ticktick-to-sqlite/releases)
[![Tests](https://github.com/Scarvy/ticktick-to-sqlite/actions/workflows/test.yml/badge.svg)](https://github.com/Scarvy/ticktick-to-sqlite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Scarvy/ticktick-to-sqlite/blob/master/LICENSE)

Import TickTick data into a SQLite database

## Installation

Install this tool using `pip`:

    pip install ticktick-to-sqlite

## Usage

For help, run:

    ticktick-to-sqlite --help

You can also use:

    python -m ticktick_to_sqlite --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd ticktick-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
