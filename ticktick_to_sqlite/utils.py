from ticktick.api import TickTickClient  # Main Interface
from ticktick.oauth2 import OAuth2  # OAuth2 Manager


def oauth_token(client_id, client_secret, redirect_uri):
    """Generate new access token, or retreive cached one."""
    return OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )


def uncompleted_tasks(username, password, auth_token):
    """Get uncompleted tasks from TickTick."""
    client = TickTickClient(username, password, auth_token)

    return client.state["tasks"]


def completed_tasks(username, password, auth_token, start_date, end_date=None):
    """Get completed tasks from TickTick."""
    client = TickTickClient(username, password, auth_token)

    return client.task.get_completed(start=start_date, end=end_date)


def get_tags(usernmae, password, auth_token):
    """Get tags from TickTick."""
    client = TickTickClient(usernmae, password, auth_token)
    return client.state["tags"]


def get_projects(username, password, auth_token):
    """Get projects (aka "List") in TickTick."""
    client = TickTickClient(username, password, auth_token)
    return client.state["projects"]


def get_project_folders(username, password, auth_token):
    """Get project folders (aka "List Folders") from"""
    client = TickTickClient(username, password, auth_token)
    return client.state["project_folders"]
