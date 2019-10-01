import pytest
from flask import g
from flask import session

from cms.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register',
        data={'username': 'addeduser', 'password': 'abcd1234'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert (
            get_db().execute(
                'select * from user where username = ?',
                ('addeduser',)
            ).fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('', '', b'Username is required.'),
        ('aabbccdd', '', b'Password is required.'),
        ('testuser', 'testpass', b'already registered'),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register', data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'testuser'


@pytest.mark.parametrize(
    ('username', 'password'),
    (
        ('aaaa', 'testpass'), 
        ('testuser', 'aaaa')
    ),
)
def test_login_validate_input(auth, username, password):
    response = auth.login(username, password)
    message = b'Incorrect username or password.'
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
