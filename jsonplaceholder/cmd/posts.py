from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/posts'


def view_post(post: Dict[str, Union[int, str]]) -> str:
    userId: int = typer.style(
        f'userId={post["userId"]}, ', fg=typer.colors.GREEN)
    id: int = typer.style(f'id={post["id"]}, ', fg=typer.colors.RED)
    title: str = typer.style(f'title={post["title"]}, ', fg=typer.colors.BLUE)
    body: str = typer.style(f'body={post["body"]}', fg=typer.colors.WHITE)
    return f'{id}{userId}{title}{body}'


@app.command()
def list(userId: int = typer.Option(None,
                                    help='Get posts only from the given user.',
                                    min=1,)):
    """
    List Albums.
    """
    uri = ENDPOINT if not userId else f'{ENDPOINT}?userId={userId}'
    response: requests.Response = rest.get(uri)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    posts = response.json()
    typer.echo_via_pager([f'{view_post(post)}\n' for post in posts])


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about post by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_post(response.json()))


@app.command()
def delete(id: int = typer.Argument(..., min=1)):
    """
    Delete an post by ID.
    """
    response: requests.Response = rest.delete(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to delete resource')
    typer.echo('Resource deleted successfully.')


@app.command()
def update(id: int = typer.Argument(..., min=1),
           userId: int = typer.Option(None, help='ID of the user.'),
           title: str = typer.Option(None, help='Title of the post.'),
           body: str = typer.Option(None, help='Body of the post.'),
           ):
    """
    Update an post by ID, omitted fields will be left unchanged.
    """
    post_response = rest.get(f'{ENDPOINT}/{id}')
    if post_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    post = post_response.json()
    post = {
        'userId': userId or post['userId'],
        'title': title or post['title'],
        'body': body or post['body']
    }
    response = rest.put(f'{ENDPOINT}/{id}', post)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_post(response.json()))


@app.command()
def create(userId: int = typer.Option(..., help='ID of the user.', min=1),
           title: str = typer.Option(..., help='Title of the post.'),
           body: str = typer.Option(..., help='Body of the post.'),
           ):
    """
    Create a new post.
    """
    post = {
        'userId': userId,
        'title': title,
        'body': body
    }
    response: requests.Response = rest.post(
        ENDPOINT, post)
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_post(response.json()))


@app.callback()
def main():
    """
    Manage Posts
    """


if __name__ == '__main__':
    app()
