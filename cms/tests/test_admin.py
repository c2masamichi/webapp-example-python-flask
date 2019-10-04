import pytest

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    ('/admin/create', '/admin/update/1', '/admin/delete/1')
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
