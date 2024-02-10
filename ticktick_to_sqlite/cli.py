import json
import os
import pathlib

import click
import sqlite_utils

from ticktick_to_sqlite import utils


@click.group()
@click.version_option()
def cli():
    "Import TickTick data into a SQLite database"


@cli.command(name="auth")
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save tokens and login credentials to, defaults to auth.json",
)
def auth(auth):
    "Save authentication and user credentials to a JSON file"
    click.echo(
        "Register your application and obtain: Client ID Client secret, and pick a redirect URL and Paste it here:"
    )
    click.echo("App Settings:")
    client_id = click.prompt("Client ID")
    client_secret = click.prompt("Client Secret")
    oauth_redirect_url = click.prompt("Redirect URL")

    click.echo("Get login credentials and Paste it here:")
    click.echo("User Credentials:")
    username = click.prompt("Username", "")
    password = click.prompt("Password", "")

    # not login provided, use enviornment variables
    if not username or not password:
        username, password = utils.login_credentials()

    if pathlib.Path(auth).exists():
        auth_data = json.load(open(auth))
    else:
        auth_data = {}
    auth_data["client_id"] = client_id
    auth_data["client_secret"] = client_secret
    auth_data["oauth_redirect_url"] = oauth_redirect_url
    auth_data["username"] = username
    auth_data["password"] = password
    open(auth, "w").write(json.dumps(auth_data, indent=4) + "\n")


@cli.command(name="login")
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save login credentials to, defaults to auth.json",
)
def login(auth):
    """Update login credentials."""
    click.echo("Get login credentials and Paste it here:")
    click.echo("User Credentials:")
    username = click.prompt("Username", "")
    password = click.prompt("Password", "")

    if pathlib.Path(auth).exists():
        auth_data = json.load(open(auth))
    else:
        auth_data = {}
    auth_data["username"] = username
    auth_data["password"] = password

    open(auth, "w").write(json.dumps(auth_data, indent=4) + "\n")


@cli.command(name="tasks")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to OAuth token file",
)
def tasks(db_path, auth):
    "Fetch all uncompleted tasks."

    db = sqlite_utils.Database(db_path)

    token = load_token(auth)
    username, password = load_login_creds(auth)

    uncompleted_tasks = utils.uncompleted_tasks(username, password, token)

    uncompleted_tasks_table = db.table("uncompleted_tasks", pk="id")
    uncompleted_tasks_table.upsert_all(uncompleted_tasks, alter=True)


@cli.command(name="completed tasks")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "-s" "start_date",
    type=click.DateTime(),
    required=True,
)
@click.argument(
    "-e" "end_date",
    type=click.DateTime(),
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to OAuth token file",
)
def completed_tasks(db_path, start_date, end_date, auth):
    "Fetch completed tasks."
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)
    username, password = load_login_creds()
    completed_tasks = utils.completed_tasks(
        username, password, token, start_date, end_date
    )

    completed_tasks_table = db.table("completed_tasks", pk="id")
    completed_tasks_table.upsert_all(completed_tasks, alter=True)


@cli.command(name="tags")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to OAuth token file",
)
def tags(db_path, auth):
    "Fetch tags."
    db = sqlite_utils.Database(db_path)

    token = load_token(auth)
    username, password = load_login_creds()

    tags = utils.get_tags(username, password, token)

    tags_table = db.table("tags", pk="name")
    tags_table.upsert_all(tags, alter=True)


@cli.command(name="projects")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to OAuth token file",
)
def projects(db_path, auth):
    "Fetch projects."
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)
    username, password = load_login_creds()

    projects = utils.get_projects(username, password, token)

    projects_table = db.table("projects", pk="id")
    projects_table.upsert_all(projects, alter=True)


@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to OAuth token file",
)
def project_folders(db_path, auth):
    """Fetch project folders"""
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)
    username, password = load_login_creds()

    project_folders = utils.get_project_folders(username, password, token)

    project_folders_table = db.table("projects", pk="id")
    project_folders_table.upsert_all(project_folders, alter=True)


# source: https://github.com/dogsheep/github-to-sqlite/blob/eaef8ffd3f46be6c26062237ed88b4c2202a1c44/github_to_sqlite/cli.py#L640C1-L648C17
def load_token(auth):
    try:
        client_id = json.load(open(auth))["client_id"]
        client_secret = json.load(open(auth))["client_secret"]
        redirect_url = json.load(open(auth))["redirect_url"]
    except (KeyError, FileNotFoundError):
        token = None
    if token is None:
        # Fallback to TICKTICK_ environment variables
        client_id = os.environ.get("TICKTICK_CLIENT_ID") or None
        client_secret = os.environ.get("TICKTICK_CLIENT_SECRET") or None
        redirect_url = os.environ.get("TICKTICK_REDIRECT_URL") or None
    return utils.oauth_token(client_id, client_secret, redirect_url)


def load_login_creds(auth):
    try:
        username = json.load(open(auth))["username"]
        password = json.load(open(auth))["password"]
    except (KeyError, FileNotFoundError):
        username = None
        password = None
    if username is None and password is None:
        username, password = login_credentials()
    return username, password


def login_credentials():
    try:
        username = os.environ["TICKTICK_USERNAME"]
    except KeyError as e:
        print("Enviornment variable TICKTICK_USERNAME does not exist.", e)
    try:
        password = os.environ["TICKTICK_PASSWORD"]
    except KeyError as e:
        print("Enviornment variable TICKTICK_PASSWORD does not exist.", e)
    return username, password
