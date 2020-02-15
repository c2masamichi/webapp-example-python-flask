import pytest

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/user/create',
    )
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_create(client, auth, app):
    auth.login()
    assert client.get('/user/create').status_code == 200

    response = client.post(
        '/user/create',
        data={'username': 'addeduser', 'password': 'abcd1234'}
    )
    assert 'http://localhost/user/' == response.headers['Location']

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where username = %s',
                ('addeduser',)
            )
            user = cursor.fetchone()
        assert user is not None


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('', '', b'Username is required.'),
        ('aabbccdd', '', b'Password is required.'),
        ('testuser', 'testpass', b'already registered'),
    ),
)
def test_create_validate_input(client, auth, username, password, message):
    auth.login()
    response = client.post(
        '/user/create', data={'username': username, 'password': password}
    )
    assert message in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/user/delete/1')
    assert response.headers['Location'] == 'http://localhost/user/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE id = 1')
            user = cursor.fetchone()
        assert user is None
