from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/comments'


def view_comment(comment: Dict[str, Union[int, str]]) -> str:
    postId: int = typer.style(
        f'postId={comment["postId"]}, ', fg=typer.colors.GREEN)
    id: int = typer.style(f'id={comment["id"]}, ', fg=typer.colors.RED)
    name: str = typer.style(f'name={comment["name"]}, ', fg=typer.colors.BLUE)
    email: str = typer.style(
        f'email={comment["email"]}, ', fg=typer.colors.GREEN)
    body: str = typer.style(f'body={comment["body"]}', fg=typer.colors.WHITE)
    return f'{id}{postId}{name}{email}{body}'


@app.command()
def list(postId: int = typer.Option(None,
                                    help='Get comments only from the given post.',
                                    min=1,)):
    """
    List Comments.
    """
    uri = ENDPOINT if not postId else f'{ENDPOINT}?postId={postId}'
    response: requests.Response = rest.get(uri)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    comments = response.json()
    typer.echo_via_pager(
        [f'{view_comment(comment)}\n' for comment in comments])


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about comment by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_comment(response.json()))


@app.command()
def delete(id: int = typer.Argument(..., min=1)):
    """
    Delete an album by ID.
    """
    response: requests.Response = rest.delete(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to delete resource')
    typer.echo('Resource deleted successfully.')


@app.command()
def update(id: int = typer.Argument(..., min=1),
           postId: int = typer.Option(None, help='ID of the post.'),
           name: str = typer.Option(None, help='Name of the comment.'),
           email: str = typer.Option(None, help='E-mail address'),
           body: str = typer.Option(None, help='Body of the comment.'),
           ):
    """
    Update an comment by ID, omitted fields will be left unchanged.
    """
    comment_response = rest.get(f'{ENDPOINT}/{id}')
    if comment_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    comment = comment_response.json()
    comment = {
        'postId': postId or comment['postId'],
        'name': name or comment['name'],
        'email': email or comment['email'],
        'body': body or comment['body']
    }
    response = rest.put(f'{ENDPOINT}/{id}', comment)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_comment(response.json()))


@app.command()
def create(postId: int = typer.Option(..., help='ID of the post.', min=1),
           name: str = typer.Option(..., help='Name of the comment.'),
           email: str = typer.Option(..., help='E-mail address'),
           body: str = typer.Option(..., help='Body of the comment.'),
           ):
    """
    Create a comment.
    """
    comment = {
        'postId': postId,
        'name': name,
        'email': email,
        'body': body
    }
    response: requests.Response = rest.post(
        ENDPOINT, comment)
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_comment(response.json()))


@app.callback()
def main():
    """
    Manage Comments
    """


if __name__ == '__main__':
    app()
