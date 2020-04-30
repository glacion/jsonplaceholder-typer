from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/photos'


def view_photo(photo: Dict[str, Union[int, str]]) -> str:
    albumId: int = typer.style(
        f'albumId={photo["albumId"]}, ', fg=typer.colors.GREEN)
    id: int = typer.style(f'id={photo["id"]}, ', fg=typer.colors.RED)
    title: str = typer.style(f'title={photo["title"]}, ', fg=typer.colors.BLUE)
    url: str = typer.style(
        f'url={photo["url"]}, ', fg=typer.colors.GREEN)
    thumbnailUrl: str = typer.style(
        f'thumbnailUrl={photo["thumbnailUrl"]}', fg=typer.colors.RED)
    return f'{id}{albumId}{title}{url}{thumbnailUrl}'


@app.command()
def list(albumId: int = typer.Option(None,
                                     help='Get photos only from the given album.',
                                     min=1,)
         ):
    """
    List Photos.
    """
    uri = ENDPOINT if not albumId else f'{ENDPOINT}?albumId={albumId}'
    response: requests.Response = rest.get(uri)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    photos = response.json()
    typer.echo_via_pager(
        [f'{view_photo(photo)}\n' for photo in photos])


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about photo by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_photo(response.json()))


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
           albumId: int = typer.Option(None, help='ID of the album.'),
           title: str = typer.Option(None, help='Name of the photo.'),
           url: str = typer.Option(None, help='URL address'),
           thumbnailUrl: str = typer.Option(
               None, help='Thumbnail URL address.'),
           ):
    """
    Update an photo by ID, omitted fields will be left unchanged.
    """
    photo_response = rest.get(f'{ENDPOINT}/{id}')
    if photo_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    photo = photo_response.json()
    photo = {
        'albumId': albumId or photo['albumId'],
        'title': title or photo['title'],
        'url': url or photo['url'],
        'thumbnailUrl': thumbnailUrl or photo['thumbnailUrl']
    }
    response = rest.put(f'{ENDPOINT}/{id}', photo)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_photo(response.json()))


@app.command()
def create(albumId: int = typer.Option(..., help='ID of the album.', min=1),
           title: str = typer.Option(..., help='Name of the photo.'),
           url: str = typer.Option(..., help='URL of the photo'),
           thumbnailUrl: str = typer.Option(...,
                                            help='Thumbnail URL address of the photo.'),
           ):
    """
    Create a photo.
    """
    photo = {
        'albumId': albumId,
        'title': title,
        'url': url,
        'thumbnailUrl': thumbnailUrl
    }
    response: requests.Response = rest.post(
        ENDPOINT, photo)
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_photo(response.json()))


@app.callback()
def main():
    """
    Manage Photos
    """


if __name__ == '__main__':
    app()
