from http import HTTPStatus

from fast_zero.schemas import UserPublic

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


def test_create_user_name_exists(client, user):
    data = {
        'username': 'Teste',
        'email': 'teste@teste.com',
        'password': 'testtest',
    }
    response = client.post(
        URL_BASE,
        json=data,
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_email_exists(client, user):
    data = {
        'username': 'Teste2',
        'email': 'teste@teste.com',
        'password': 'testtest',
    }
    response = client.post(
        URL_BASE,
        json=data,
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_read_users(client):
    response = client.get(URL_BASE)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(URL_BASE)
    assert response.json() == {'users': [user_schema]}


def test_get_user_should_return_not_found__exercicio(client, user):
    endpoint = f'{URL_BASE}/999'
    response = client.get(endpoint)

    assert response.json() == {'detail': 'User not found'}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user___exercicio(client, user):
    endpoint = f'{URL_BASE}/{user.id}'
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_update_user(client, user):
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


def test_update_user_not_found(client):
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


def test_link_update_not_found(client):
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


def test_delete_user(client, user):
    endpoint = f'{URL_BASE}/{user.id}/'
    response = client.delete(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_link_delete_not_found(client):
    user_id = 1
    endpoint = f'{URL_BASE}/{user_id}/'

    response = client.delete(endpoint)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        URL_BASE,
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )
    response_update = client.put(
        f'{URL_BASE}/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists',
    }
