from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_returns_ok_and_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_html_returns_html():
    client = TestClient(app)

    response = client.get('/html')

    assert response.status_code == 200
    assert response.text == 'Olá Mundo!'


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
