from typing import Dict

import requests

URI = 'https://jsonplaceholder.typicode.com'


def get(endpoint: str) -> Dict[str, any]:
    """Retrieves resource from jsonplaceholder at given endpoint.

    Args:
        endpoint: Endpoint of the resource to get.

    Returns:
        JSON Representation of the resource.
    """
    pass


def post(endpoint: str, body: Dict[str, any]) -> Dict[str, any]:
    """Posts resource to jsonplaceholder at given endpoint. 

    Args:
        endpoint: Endpoint of the resource to post the body.
        body: Resource to post.

    Returns:
        JSON Representation of the resource.
    """
    pass


def put(endpoint: str, body: Dict[str, any]) -> Dict[str, any]:
    """Updates resource in jsonplaceholder at given endpoint.

    Args:
        endpoint: Endpoint of the resource to be updated.
        body: Updated state of the resource.

    Returns:
        JSON Representation of the resource.
    """
    pass


def delete(endpoint: str) -> Dict[str, any]:
    """
    Deletes resource from jsonplaceholder at given endpoint.

    Returns:
        JSON Representation of the resource.
    """
    pass
