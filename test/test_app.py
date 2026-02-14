from http import HTTPStatus

URL_BASE = '/users'


def test_create_user(client):
    response = client.post(
        URL_BASE,
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


def test_endpoint_create_not_found(client):
    endpoint = '/users_create/'
    data = {
        'username': 'alice',
        'email': 'test@test.com',
        'password': 'test',
    }
    response = client.put(
        endpoint,
        json=data,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_users(client):
    response = client.get(URL_BASE)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_get_user_should_return_not_found__exercicio(client):
    user_id = 666
    endpoint = f'/users/{user_id}'
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user___exercicio(client):
    user_id = 1
    endpoint = f'/users/{user_id}'
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_update_user(client):
    user_id = 1
    endpoint = f'{URL_BASE}/{user_id}/'
    response = client.put(
        endpoint,
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


def test_update_not_found(client):
    user_id = 2
    endpoint = f'{URL_BASE}/{user_id}/'
    response = client.put(
        endpoint,
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    user_id = 1
    endpoint = f'{URL_BASE}/{user_id}/'
    response = client.delete(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found(client):
    user_id = 1
    endpoint = f'{URL_BASE}/{user_id}/'

    response = client.delete(endpoint)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
