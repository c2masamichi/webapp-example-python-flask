import pytest
from flask import g
from flask import session
from werkzeug.security import check_password_hash

from cms.models import User


def test_login(client, auth):
    assert client.get('/admin/login').status_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/admin/'

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
    assert b'Incorrect username or password.' in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


@pytest.mark.parametrize(
    'path',
    (
        '/admin/',
        '/admin/password_change/',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


def test_admin_top(client, auth):
    auth.login()
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Users' in response.data
    assert b'Edit' in response.data

    auth.login(role='editor')
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Users' not in response.data
    assert b'Edit' in response.data

    auth.login(role='author')
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Users' not in response.data
    assert b'Edit' in response.data


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
        user = User.query.get(1)
        assert check_password_hash(user.password, new_password)


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
