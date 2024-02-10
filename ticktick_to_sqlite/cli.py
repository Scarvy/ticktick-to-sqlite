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
    help="Path to save tokens to, defaults to auth.json",
)
def auth(auth):
    "Save authentication credentials to a JSON file"
    click.echo(
        "Register your application and obtain a client ID and client secret and paste it here:"
    )
    click.echo()
    client_id = click.prompt("Client ID")
    client_secret = click.prompt("Client Secret")
    oauth_redirect_url = click.prompt("Redirect URL")
    if pathlib.Path(auth).exists():
        auth_data = json.load(open(auth))
    else:
        auth_data = {}
    auth_data["client_id"] = client_id
    auth_data["client_secret"] = client_secret
    auth_data["oauth_redirect_url"] = oauth_redirect_url
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
    default=".token.oauth",
    help="Path to OAuth token file",
)
def tasks(db_path, auth):
    "Fetch all uncompleted tasks."

    db = sqlite_utils.Database(db_path)

    token = load_token(auth)

    uncompleted_tasks = utils.uncompleted_taks(token)

    uncompleted_tasks_table = db.table("uncompleted_tasks", pk="id")
    uncompleted_tasks_table.upsert_all(uncompleted_tasks, alter=True)
    uncompleted_tasks_table.add_foreign_key("projectId", "projects", "id")


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
    default=".token.oauth",
    help="Path to OAuth token file",
)
def completed_tasks(db_path, start_date, end_date, auth):
    "Fetch completed tasks."
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)
    completed_tasks = utils.completed_tasks(token, start_date, end_date)

    completed_tasks_table = db.table("completed_tasks", pk="id")
    completed_tasks_table.upsert_all(completed_tasks, alter=True)
    completed_tasks_table.add_foreign_key("projectId", "projects", "id")


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
    default=".token.oauth",
    help="Path to OAuth token file",
)
def tags(db_path, auth):
    "Fetch tags."
    db = sqlite_utils.Database(db_path)

    token = load_token(auth)

    tags = utils.get_tags(token)

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
    default=".token.oauth",
    help="Path to OAuth token file",
)
def projects(db_path, auth):
    "Fetch projects."
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)

    projects = utils.get_projects(token)

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
    default=".token.oauth",
    help="Path to OAuth token file",
)
def project_folders(db_path, auth):
    """Fetch project folders"""
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)

    project_folders = utils.get_project_folders(token)

    project_folders_table = db.table("projects", pk="id")
    project_folders_table.upsert_all(project_folders, alter=True)


# source: https://github.com/dogsheep/github-to-sqlite/blob/eaef8ffd3f46be6c26062237ed88b4c2202a1c44/github_to_sqlite/cli.py#L640C1-L648C17
def load_token(auth):
    try:
        token = json.load(open(auth))["github_personal_token"]
    except (KeyError, FileNotFoundError):
        token = None
    if token is None:
        # Fallback to GITHUB_TOKEN environment variable
        token = os.environ.get("GITHUB_TOKEN") or None
    return token
