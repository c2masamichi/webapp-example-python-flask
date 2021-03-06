import pytest
from werkzeug.security import check_password_hash

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/admin/auth/user/',
        '/admin/auth/user/add/',
        '/admin/auth/user/2/change/',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


@pytest.mark.parametrize(
    'path',
    (
        '/admin/auth/user/add/',
        '/admin/auth/user/2/change/',
        '/admin/auth/user/2/password/',
        '/admin/auth/user/2/delete/',
    )
)
def test_login_required_post(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


@pytest.mark.parametrize(
    'path',
    (
        '/admin/auth/user/',
        '/admin/auth/user/add/',
        '/admin/auth/user/2/change/',
    )
)
def test_admin_required_get(client, auth, path):
    auth.login(role='editor')
    response = client.get(path)
    assert response.status_code == 403

    auth.login(role='author')
    response = client.get(path)
    assert response.status_code == 403


@pytest.mark.parametrize(
    'path',
    (
        '/admin/auth/user/add/',
        '/admin/auth/user/2/change/',
        '/admin/auth/user/2/password/',
        '/admin/auth/user/2/delete/',
    )
)
def test_admin_required_post(client, auth, path):
    auth.login(role='editor')
    response = client.post(path)
    assert response.status_code == 403

    auth.login(role='author')
    response = client.post(path)
    assert response.status_code == 403


@pytest.mark.parametrize(
    'path',
    (
        '/admin/auth/user/10/change/',
        '/admin/auth/user/10/password/',
        '/admin/auth/user/10/delete/'
    )
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_index(client, auth):
    auth.login()
    response = client.get('/admin/auth/user/')
    assert response.status_code == 200
    assert b'user-admin01' in response.data


def test_create(client, auth, app):
    path = '/admin/auth/user/add/'
    auth.login()
    assert client.get(path).status_code == 200

    role = 'administrator'
    username = 'added-user_01'
    password = 'ab-cd_1234'
    response = client.post(
        path,
        data={'role': role, 'username': username, 'password': password}
    )
    assert response.status_code == 302
    assert 'http://localhost/admin/auth/user/' == response.headers['Location']

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE username = %s',
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
    path = '/admin/auth/user/add/'
    role = 'administrator'
    auth.login()
    response = client.post(
        path,
        data={'role': role, 'username': username, 'password': password}
    )
    assert message in response.data


def test_update(client, auth, app):
    user_id = 2
    role = 'author'
    username = 'updated-to-author02'
    path = '/admin/auth/user/{0}/change/'.format(user_id)

    auth.login()
    assert client.get(path).status_code == 200
    response = client.post(path, data={'role': role, 'username': username})
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost{0}'.format(path)

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE id = %s',
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
    path = '/admin/auth/user/{0}/change/'.format(user_id)
    auth.login()
    response = client.post(path, data={'role': role, 'username': username})
    assert message in response.data


def test_chpasswd(client, auth, app):
    user_id = 2
    new_password = 'updated-pass_01'
    path = '/admin/auth/user/{0}/password/'.format(user_id)
    auth.login()
    response = client.post(
        path,
        data={'new_password': new_password}
    )
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert check_password_hash(user['password'], new_password)


@pytest.mark.parametrize(
    ('new_password', 'message'),
    (
        ('a' * 31, b'Bad data'),
        ('ef-gh_5678%', b'Bad data'),
    ),
)
def test_chpasswd_validate(client, auth, new_password, message):
    user_id = 2
    path = '/admin/auth/user/{0}/password/'.format(user_id)
    auth.login()
    response = client.post(
        path,
        data={'new_password': new_password}
    )
    assert message in response.data


def test_delete(client, auth, app):
    user_id = 2
    path = '/admin/auth/user/{0}/delete/'.format(user_id)
    auth.login()
    response = client.post(path)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/admin/auth/user/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM user WHERE id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert user is None
