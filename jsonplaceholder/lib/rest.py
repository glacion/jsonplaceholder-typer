from typing import Dict

import requests

URI = 'https://jsonplaceholder.typicode.com'


def get(endpoint: str) -> requests.Response:
    """Retrieves resource from jsonplaceholder at given endpoint.

    Args:
        endpoint: Endpoint of the resource to get.

    Returns:
        JSON Representation of the resource.
    """
    return requests.get(f'{URI}{endpoint}')


def post(endpoint: str, body: Dict[str, any]) -> requests.Response:
    """Posts resource to jsonplaceholder at given endpoint. 

    Args:
        endpoint: Endpoint of the resource to post the body.
        body: Resource to post.

    Returns:
        JSON Representation of the resource.
    """
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    return requests.post(f'{URI}{endpoint}', json=body, headers=headers)


def put(endpoint: str, body: Dict[str, any]) -> requests.Response:
    """Updates resource in jsonplaceholder at given endpoint.

    Args:
        endpoint: Endpoint of the resource to be updated.
        body: Updated state of the resource.

    Returns:
        JSON Representation of the resource.
    """
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    return requests.put(f'{URI}{endpoint}', json=body, headers=headers)


def delete(endpoint: str) -> requests.Response:
    """
    Deletes resource from jsonplaceholder at given endpoint.

    Returns:
        JSON Representation of the resource.
    """
    return requests.delete(f'{URI}{endpoint}')
