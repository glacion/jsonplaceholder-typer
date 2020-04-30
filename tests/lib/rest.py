import requests

import jsonplaceholder.lib.rest
import pytest


def test_get_posts_correctly():
    response: requests.Response = jsonplaceholder.lib.rest.get('/posts')
    assert response != None
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 100
    assert posts[0]['id'] == 1
    assert posts[0]['userId'] == 1


def test_get_post_correctly():
    response: requests.Response = jsonplaceholder.lib.rest.get('/posts/42')
    assert response != None
    assert response.status_code == 200
    post = response.json()
    assert len(post) == 4
    assert post['id'] == 42
    assert post['userId'] == 5


def test_get_post_with_invalid_id_returns_404():
    response: requests.Response = jsonplaceholder.lib.rest.get(
        '/posts/422')
    assert response != None
    assert response.status_code == 404


def test_post_todo_correctly():
    response: requests.Response = jsonplaceholder.lib.rest.post(
        '/todos', {'userId': 1, 'title': 'finish coding', 'completed': 'false'})
    assert response != None
    assert response.status_code == 201
    todo = response.json()
    assert todo['userId'] == 1
    assert todo['title'] == 'finish coding'
    assert todo['completed'] == 'false'


def test_post_todo_discards_id():
    response: requests.Response = jsonplaceholder.lib.rest.post(
        '/todos', {'id': 12, 'userId': 1, 'title': 'finish coding', 'completed': 'false'})
    assert response != None
    assert response.status_code == 201
    todo = response.json()
    assert todo['userId'] == 1
    assert todo['title'] == 'finish coding'
    assert todo['completed'] == 'false'
    assert todo['id'] != 12


def test_updates_photo_title():
    response = jsonplaceholder.lib.rest.put('/photos/1', {'title': 'foo'})
    assert response != None
    assert response.status_code == 200
    assert response.json()['title'] == 'foo'


def test_id_is_immutable():
    response = jsonplaceholder.lib.rest.put('/photos/1', {'id': 123})
    assert response != None
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_deletes_user():
    response: requests.Response = jsonplaceholder.lib.rest.delete(
        '/users/1')
    assert response != None
    assert response.status_code == 200
