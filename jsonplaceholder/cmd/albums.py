from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/albums'


def view_album(album: Dict[str, Union[int, str]]) -> str:
    userId: int = typer.style(
        f'userId={album["userId"]}, ', fg=typer.colors.GREEN)
    id: int = typer.style(f'id={album["id"]}, ', fg=typer.colors.RED)
    title: str = typer.style(f'title={album["title"]}', fg=typer.colors.BLUE)
    return f'{id}{userId}{title}'


@app.command()
def list(userId: int = typer.Option(None, help='Get albums only from the given user.', min=1)):
    """
    List all Albums.
    """
    uri = ENDPOINT if not userId else f'{ENDPOINT}?userId={userId}'
    response: requests.Response = rest.get(uri)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    albums = response.json()
    typer.echo_via_pager([f'{view_album(album)}\n' for album in albums])


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about album by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_album(response.json()))


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
           userId: int = typer.Option(None, help='ID of the user.'),
           title: str = typer.Option(None, help='Title of the album.'),
           ):
    """
    Update an album by ID, omitted fields will be left unchanged.
    """
    album_response = rest.get(f'{ENDPOINT}/{id}')
    if album_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    album = album_response.json()
    album = {
        'userId': userId or album['userId'],
        'title': title or album['title']
    }
    response = rest.put(f'{ENDPOINT}/{id}', album)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_album(response.json()))


@app.command()
def create(userId: int = typer.Option(..., help='ID of the user.', min=1),
           title: str = typer.Option(..., help='Title of the album.'),
           ):
    """
    Create a new album.
    """
    response: requests.Response = rest.post(
        f'{ENDPOINT}', {'userId': userId, 'title': title})
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_album(response.json()))


@app.callback()
def main():
    """
    Manage Albums
    """


if __name__ == '__main__':
    app()
