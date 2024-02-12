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

**Pre-requisite:**

1. Register your application.

    * Assuming you have a TickTick account, register your app and create a `client_id` and `client_secret`.

        > @lazeroffmichael (author of `ticktick-py`) wrote a easy to follow ["Get Started"](https://lazeroffmichael.github.io/ticktick-py/#get-started) instructions to set up your app.

2. (Recommended) Set enviornment variables for your login credentials:
    * `TICKTICK_USERNANE` - Your TickTick username
    * `TICKTICK_PASSWORD` - Your TickTick password

For help, run:

    ticktick-to-sqlite --help

You can also use:

    python -m ticktick_to_sqlite --help

### Authenticate

Store app settings for OAuth.

    (venv) $ ticktick-to-sqlite auth
    Register your application and obtain: "Client ID", "Client Secret", and pick a "Redirect URL". Paste it here:

    Client ID: your_client_id
    Client Secret: your_client_secret
    Redirect URL: https://127.0.0.1

### Tasks

Save your uncompleted tasks.

    ticktick-to-sqlite tasks ticktick.db

Save your completed tasks for a specified time range (ex. between Dec 31st, 2023 and Jan 31st, 2024).

    ticktick-to-sqlite completed-tasks ticktick.db 2023-12-31 --end-date 2024-01-31

### Tags

Save your tags.

    ticktick-to-sqlite tags ticktick.db

### Projects

Save your projects (aka "Lists").

    ticktick-to-sqlite projects

Save your project folders (aka "List Folders").

    ticktick-to-sqlite project-folders

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd ticktick-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
