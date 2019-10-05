import pytest

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/admin/create',
        '/admin/update/1',
        '/admin/delete/1',
        '/admin/register',
    )
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize(
    'path',
    ('/admin/update/5', '/admin/delete/5')
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/admin/create').status_code == 200
    client.post(
        '/admin/create',
        data={'title': 'created', 'body': 'created on test'}
    )

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 4').fetchone()
        assert post['title'] == 'created'
        assert post['body'] == 'created on test'


def test_update(client, auth, app):
    auth.login()
    assert client.get('/admin/update/1').status_code == 200
    client.post(
        '/admin/update/1',
        data={'title': 'updated', 'body': 'updated on test'}
    )

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'
        assert post['body'] == 'updated on test'


@pytest.mark.parametrize(
    'path',
    ('/admin/create', '/admin/update/1')
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/admin/delete/1')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None


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
