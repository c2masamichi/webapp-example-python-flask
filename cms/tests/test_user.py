import pytest

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/admin/register',
    )
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_register(client, auth, app):
    auth.login()
    assert client.get('/admin/register').status_code == 200

    response = client.post(
        '/admin/register',
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
def test_register_validate_input(client, auth, username, password, message):
    auth.login()
    response = client.post(
        '/admin/register', data={'username': username, 'password': password}
    )
    assert message in response.data
