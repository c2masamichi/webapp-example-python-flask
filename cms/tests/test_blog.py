import pytest

from cms.db import get_db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Title 1' in response.data
    assert b'2019-01-01' in response.data


def test_get_entry(client):
    response = client.get('/entry/1')
    assert response.status_code == 200
    assert b'Test Title 1' in response.data
    assert b'2019-01-01' in response.data
    assert b'This body is test.' in response.data


def test_get_entry_exists_required(client):
    response = client.get('/entry/10')
    assert response.status_code == 404


@pytest.mark.parametrize(
    'path',
    (
        '/admin/blog/entry/',
        '/admin/blog/entry/add/',
        '/admin/blog/entry/2/change',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


@pytest.mark.parametrize(
    'path',
    (
        '/admin/blog/entry/add/',
        '/admin/blog/entry/2/change',
        '/admin/blog/entry/2/delete',
    )
)
def test_login_required_post(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


@pytest.mark.parametrize(
    'path',
    (
        '/admin/blog/entry/10/change',
        '/admin/blog/entry/10/delete',
    )
)
def test_exists_required_post(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_edit_top(client, auth):
    auth.login()
    response = client.get('/admin/blog/entry/')
    assert response.status_code == 200
    assert b'Test Title 2' in response.data
    assert b'2019-01-01' in response.data
    assert b'user-editor01' in response.data


def test_create(client, auth, app):
    path = '/admin/blog/entry/add/'
    auth.login()
    assert client.get(path).status_code == 200

    title = 'created'
    body = 'created on test'
    response = client.post(
        path,
        data={'title': title, 'body': body}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/admin/blog/entry/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 4')
            entry = cursor.fetchone()
        assert entry['author_id'] == 1
        assert entry['title'] == title
        assert entry['body'] == body


def test_update(client, auth, app):
    entry_id = 2
    title = 'updated'
    body = 'updated on test'
    path = '/admin/blog/entry/{0}/change'.format(entry_id)

    auth.login()
    assert client.get(path).status_code == 200
    response = client.post(
        path,
        data={'title': title, 'body': body}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost{0}'.format(path)

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM entry WHERE id = %s',
                (entry_id,)
            )
            entry = cursor.fetchone()
        assert entry['title'] == title
        assert entry['body'] == body


@pytest.mark.parametrize(
    'path',
    (
        '/admin/blog/entry/add/',
        '/admin/blog/entry/2/change',
    )
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

    response = client.post(path, data={'title': 'a' * 101, 'body': ''})
    assert b'Bad data' in response.data


def test_delete(client, auth, app):
    entry_id = 2
    auth.login()
    response = client.post('/admin/blog/entry/{0}/delete'.format(entry_id))
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/admin/blog/entry/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM entry WHERE id = %s',
                (entry_id,)
            )
            entry = cursor.fetchone()
        assert entry is None


def test_update_own_entry(client, auth, app):
    title = 'updated'
    body = 'updated on test'
    own_entry_id = 3
    others_entry_id = 1  # author is user-admin01

    # role=author: can update own entries, but not others' entries
    auth.login(role='author')
    path = '/admin/blog/entry/{0}/change'.format(own_entry_id)
    assert client.get(path).status_code == 200
    response = client.post(
        path,
        data={'title': title, 'body': body}
    )
    assert response.status_code == 302

    path = '/admin/blog/entry/{0}/change'.format(others_entry_id)
    assert client.get(path).status_code == 403
    response = client.post(
        path,
        data={'title': title, 'body': body}
    )
    assert response.status_code == 403

    # role=editor: can update others' entries
    auth.login(role='editor')
    path = '/admin/blog/entry/{0}/change'.format(others_entry_id)
    assert client.get(path).status_code == 200
    response = client.post(
        path,
        data={'title': title, 'body': body}
    )
    assert response.status_code == 302


def test_delete_own_entry(client, auth, app):
    own_entry_id = 3
    others_entry_id = 1  # author is user-admin01

    # role=author: can delete own entries, but not others' entries
    auth.login(role='author')
    response = client.post(
        '/admin/blog/entry/{0}/delete'.format(own_entry_id))
    assert response.status_code == 302

    response = client.post(
        '/admin/blog/entry/{0}/delete'.format(others_entry_id))
    assert response.status_code == 403

    # role=editor: can delete others' entries
    auth.login(role='editor')
    response = client.post(
        '/admin/blog/entry/{0}/delete'.format(others_entry_id))
    assert response.status_code == 302
