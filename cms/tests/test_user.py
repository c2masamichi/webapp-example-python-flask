import pytest

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/user/',
        '/user/create',
        '/user/update/2',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize(
    'path',
    (
        '/user/create',
        '/user/update/2',
        '/user/delete/2',
    )
)
def test_login_required_post(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize(
    'path',
    ('/user/update/10', '/user/delete/10')
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/user/create').status_code == 200

    role = 'administrator'
    username = 'addeduser'
    password = 'abcd1234'
    response = client.post(
        '/user/create',
        data={'role': role, 'username': username, 'password': password}
    )
    assert 'http://localhost/user/' == response.headers['Location']

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where username = %s',
                (username,)
            )
            user = cursor.fetchone()
        assert user is not None


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('', '', b'Username is required.'),
        ('aabbccdd', '', b'Password is required.'),
        ('user-admin01', 'testpass', b'already registered'),
    ),
)
def test_create_validate(client, auth, username, password, message):
    role = 'administrator'
    auth.login()
    response = client.post(
        '/user/create',
        data={'role': role, 'username': username, 'password': password}
    )
    assert message in response.data


def test_update(client, auth, app):
    user_id = 2
    role = 'author'
    username = 'updated-to-author'
    url = '/user/update/{0}'.format(user_id)

    auth.login()
    assert client.get(url).status_code == 200
    client.post(
        url, data={'role': role, 'username': username}
    )

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert user['role'] == role
        assert user['username'] == username


@pytest.mark.parametrize(
    ('username', 'message'),
    (
        ('', b'Username is required.'),
        ('user-admin01', b'already registered'),
    ),
)
def test_update_validate(client, auth, username, message):
    user_id = 2
    role = 'administrator'
    url = '/user/update/{0}'.format(user_id)
    auth.login()
    response = client.post(
        url, data={'role': role, 'username': username}
    )
    assert message in response.data


def test_delete(client, auth, app):
    user_id = 2
    auth.login()
    response = client.post('/user/delete/{0}'.format(user_id))
    assert response.headers['Location'] == 'http://localhost/user/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert user is None
