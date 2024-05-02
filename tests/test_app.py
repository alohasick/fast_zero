from http import HTTPStatus

from fast_zero.models import User
import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.schemas import UserPublic


def test_root_returns_ok_and_hello_world(client: TestClient):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_html_returns_html(client: TestClient):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert response.text == 'Olá Mundo!'


def test_create_user(client: TestClient):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client: TestClient):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_get_user_from_id(client: TestClient, user: User):
    response = client.get('/users/1')
    user_schema = UserPublic.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


@pytest.mark.parametrize('user_id', [-1, 2], ids=['user_id: -1', 'user_id: 2'])
def test_get_not_found_user(client: TestClient, user_id: int):
    response = client.get(f'/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client: TestClient, user: User):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


@pytest.mark.parametrize('user_id', [-1, 1], ids=['user_id: -1', 'user_id: 2'])
def test_update_user_not_found(client: TestClient, user_id: int):
    response = client.put(
        f'/users/{user_id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client: TestClient, user: User):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.parametrize('user_id', [-1, 1], ids=['user_id: -1', 'user_id: 1'])
def test_delete_user_not_found(client: TestClient, user_id: int):
    response = client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
