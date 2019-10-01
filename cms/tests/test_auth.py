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
