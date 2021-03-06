import pytest
from flask import g
from flask import session
from werkzeug.security import check_password_hash

from cms.db import get_db


def test_login(client, auth):
    assert client.get('/admin/login').status_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'user-admin01'


@pytest.mark.parametrize(
    ('username', 'password'),
    (
        ('aaaa', 'testpass'),
        ('user-admin01', 'aaaa')
    ),
)
def test_login_validate(client, username, password):
    response = client.post(
        '/admin/login',
        data={'username': username, 'password': password}
    )
    message = b'Incorrect username or password.'
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


@pytest.mark.parametrize(
    'path',
    (
        '/admin/password_change/',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


def test_chpasswd(client, auth, app):
    path = '/admin/password_change/'
    auth.login()
    assert client.get(path).status_code == 200

    old_password = 'testpass'
    new_password = 'updated-pass_01'
    response = client.post(
        path,
        data={'old_password': old_password, 'new_password': new_password}
    )
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE id = 1')
            user = cursor.fetchone()
        assert check_password_hash(user['password'], new_password)


def test_chpasswd_validate(client, auth, app):
    path = '/admin/password_change/'
    auth.login()
    old_password = 'aaaa'
    new_password = 'updated-pass_01'
    response = client.post(
        path,
        data={'old_password': old_password, 'new_password': new_password}
    )
    assert b'Incorrect password.' in response.data
