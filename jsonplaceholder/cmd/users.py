from typing import Dict, Union

import requests

import jsonplaceholder.lib.rest as rest
import jsonplaceholder.lib.util as util
import typer

app = typer.Typer()
ENDPOINT = '/users'


def view_user(user: Dict[str, Union[int, str]]) -> str:
    id = user['id']
    name = user['name']
    username = user['username']
    email = user['email']

    street = user['address']['street']
    suite = user['address']['suite']
    city = user['address']['city']
    zipcode = user['address']['zipcode']

    latitude = user['address']['geo']['lat']
    longitude = user['address']['geo']['lng']

    phone = user['phone']
    website = user['website']

    company_name = user['company']['name']
    catch_phrase = user['company']['catchPhrase']
    bs = user['company']['bs']
    return f'\
id={id}, name={name}, username={username}, email={email}\n\
    address=street={street}, suite={suite}, city={city}, zipcode={zipcode}\n\
    geo=lat={latitude}, lng={longitude} \n\
phone={phone}, website={website} \n\
    Company=name={company_name}, catchPhrase={catch_phrase}, bs={bs}\n'


@app.command()
def list():
    """
    List Users.
    """
    response: requests.Response = rest.get(ENDPOINT)
    if response.status_code != 200:
        util.panic(f"Request resulted in error code {response.status_code}")
    users = response.json()
    typer.echo_via_pager(map(view_user, users))


@app.command()
def get(id: int = typer.Argument(..., min=1)):
    """
    Get info about user by ID.
    """
    response: requests.Response = rest.get(f'{ENDPOINT}/{id}')
    if response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    typer.echo(view_user(response.json()))


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
           name: str = typer.Option(None, help='Name of the user.'),
           username: str = typer.Option(None, help='Username of the user.'),
           email: str = typer.Option(None, help='Email of the user.'),
           street: str = typer.Option(None, help='Street of the user.'),
           suite: str = typer.Option(None, help='Suite of the user.'),
           city: str = typer.Option(None, help='City of the user.'),
           zipcode: str = typer.Option(None, help='Zipcode of the user.'),
           latitude: float = typer.Option(None,
                                          help='Latitude of the user.',
                                          min=-90.0,
                                          max=90.0,
                                          ),
           longitude: float = typer.Option(None,
                                           help='Longitude of the user.',
                                           min=-180.0,
                                           max=180.0,
                                           ),
           phone: str = typer.Option(None, help='Phone of the user.'),
           website: str = typer.Option(None, help='Website of the user.'),
           company_name: str = typer.Option(None,
                                            '--company-name',
                                            help='Company the user works at.',
                                            ),
           catch_phrase: str = typer.Option(None,
                                            help='Catch phrase of the user\'s company'),
           bs: str = typer.Option(None, help='BS of the user\'s company'),
           ):
    """
    Update an user by ID, omitted fields will be left unchanged.
    """
    user_response = rest.get(f'{ENDPOINT}/{id}')
    if user_response.status_code != 200:
        util.panic('Failure to retrieve resource.')
    user = user_response.json()
    user = {
        'name': name or user['name'],
        'username': username or user['username'],
        'email': email or user['email'],
        'address': {
            'street': street or user['address']['street'],
            'suite': suite or user['address']['suite'],
            'city': city or user['address']['city'],
            'zipcode': zipcode or user['address']['zipcode'],
            'geo': {
                'lat': latitude or user['address']['geo']['lat'],
                'lng': longitude or user['address']['geo']['lng']
            }
        },
        'phone': phone or user['phone'],
        'website': website or user['website'],
        'company': {
            'name': company_name or user['company']['name'],
            'catchPhrase': catch_phrase or user['company']['catchPhrase'],
            'bs': bs or user['company']['bs']
        }
    }
    response = rest.put(f'{ENDPOINT}/{id}', user)
    if response.status_code != 200:
        util.panic('Failure to update resource.')
    typer.echo(view_user(response.json()))


@app.command()
def create(name: str = typer.Option(..., help='Name of the user.'),
           username: str = typer.Option(..., help='Username of the user.'),
           email: str = typer.Option(..., help='Email of the user.'),
           street: str = typer.Option(..., help='Street of the user.'),
           suite: str = typer.Option(..., help='Suite of the user.'),
           city: str = typer.Option(..., help='City of the user.'),
           zipcode: str = typer.Option(..., help='Zipcode of the user.'),
           latitude: float = typer.Option(...,
                                          help='Latitude of the user.',
                                          min=-90.0,
                                          max=90.0,
                                          ),
           longitude: float = typer.Option(...,
                                           help='Longitude of the user.',
                                           min=-180.0,
                                           max=180.0,
                                           ),
           phone: str = typer.Option(..., help='Phone of the user.'),
           website: str = typer.Option(..., help='Website of the user.'),
           company_name: str = typer.Option(...,
                                            '--company-name',
                                            help='Company the user works at.',
                                            ),
           catch_phrase: str = typer.Option(...,
                                            help='Catch phrase of the user\'s company'),
           bs: str = typer.Option(..., help='BS of the user\'s company'),
           ):
    """
    Create a user.
    """
    user = {
        'name': name,
        'username': username,
        'email': email,
        'address': {
            'street': street,
            'suite': suite,
            'city': city,
            'zipcode': zipcode,
            'geo': {
                'lat': latitude,
                'lng': longitude
            }
        },
        'phone': phone,
        'website': website,
        'company': {
            'name': company_name,
            'catchPhrase': catch_phrase,
            'bs': bs
        }
    }
    response: requests.Response = rest.post(
        ENDPOINT, user)
    if response.status_code != 201:
        util.panic('Failure to create resource.')
    typer.echo(view_user(response.json()))


@app.callback()
def main():
    """
    Manage Users
    """


if __name__ == '__main__':
    app()
