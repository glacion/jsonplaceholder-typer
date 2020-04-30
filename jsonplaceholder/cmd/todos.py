from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/todos'


def view_todo(todo: Dict[str, Union[int, str]]) -> str:
    userId: int = typer.style(
        f'userId={todo["userId"]}, ', fg=typer.colors.GREEN)
    id: int = typer.style(f'id={todo["id"]}, ', fg=typer.colors.RED)
    title: str = typer.style(f'title={todo["title"]}, ', fg=typer.colors.BLUE)
    completed: str = typer.style(
        f'completed={todo["completed"]}', fg=typer.colors.WHITE)
    return f'{id}{userId}{title}{completed}'


@app.command()
def list(userId: int = typer.Option(None,
                                    help='Get todos only from the given user.',
                                    min=1,)):
    """
    List Albums.
    """
    uri = ENDPOINT if not userId else f'{ENDPOINT}?userId={userId}'
    response: requests.Response = rest.get(uri)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    todos = response.json()
    typer.echo_via_pager([f'{view_todo(todo)}\n' for todo in todos])


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about todo by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_todo(response.json()))


@app.command()
def delete(id: int = typer.Argument(..., min=1)):
    """
    Delete an todo by ID.
    """
    response: requests.Response = rest.delete(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to delete resource')
    typer.echo('Resource deleted successfully.')


@app.command()
def update(id: int = typer.Argument(..., min=1),
           userId: int = typer.Option(None, help='ID of the user.'),
           title: str = typer.Option(None, help='Title of the todo.'),
           completed: bool = typer.Option(
    False,
    '--completed/--not-completed',
    '-c/-n',
    help='Whether the todo is completed',
    show_default=True,
),
):
    """
    Update an todo by ID, omitted fields will be left unchanged.
    """
    todo_response = rest.get(f'{ENDPOINT}/{id}')
    if todo_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    todo = todo_response.json()
    todo = {
        'userId': userId or todo['userId'],
        'title': title or todo['title'],
        'completed': completed or todo['completed']
    }
    response = rest.put(f'{ENDPOINT}/{id}', todo)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_todo(response.json()))


@app.command()
def create(userId: int = typer.Option(..., help='ID of the user.', min=1),
           title: str = typer.Option(..., help='Title of the todo.'),
           completed: bool = typer.Option(
    False,
    '--completed/--not-completed',
    '-c/-n',
    help='Whether the todo is completed',
    show_default=True,
),
):
    """
    Create a new todo.
    """
    todo = {
        'userId': userId,
        'title': title,
        'completed': completed
    }
    response: requests.Response = rest.post(
        ENDPOINT, todo)
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_todo(response.json()))


@app.callback()
def main():
    """
    Manage Posts
    """


if __name__ == '__main__':
    app()
