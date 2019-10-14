import pytest
from flask import g
from flask import session

from cms.db import get_db


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
