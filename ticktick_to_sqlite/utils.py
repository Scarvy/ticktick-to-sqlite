import os

from ticktick.api import TickTickClient  # Main Interface
from ticktick.oauth2 import OAuth2  # OAuth2 Manager


def create_oauth_token(client_id, client_secret, redirect_uri):
    auth_client = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    return auth_client


def uncompleted_tasks(auth_token: dict):
    """Get uncompleted tasks from TickTick."""
    client = TickTickClient(
        os.environ["TICKTICK_USERNAME"], os.environ["TICKTICK_PASSWORD"], auth_token
    )

    return client.state["tasks"]


def completed_tasks(auth_token, start_date, end_date=None):
    """Get completed tasks from TickTick."""
    client = TickTickClient(
        os.environ["TICKTICK_USERNAME"], os.environ["TICKTICK_PASSWORD"], auth_token
    )

    return client.task.get_completed(start=start_date, end=end_date)


def get_tags(auth_token):
    client = TickTickClient(
        os.environ["TICKTICK_USERNAME"], os.environ["TICKTICK_PASSWORD"], auth_token
    )

    return client.state["tags"]


def get_projects(auth_token):
    client = TickTickClient(
        os.environ["TICKTICK_USERNAME"], os.environ["TICKTICK_PASSWORD"], auth_token
    )

    return client.state["projects"]


def get_project_folders(auth_token):
    client = TickTickClient(
        os.environ["TICKTICK_USERNAME"], os.environ["TICKTICK_PASSWORD"], auth_token
    )

    return client.state["project_folders"]
