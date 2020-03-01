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


def test_get_entry_error(client):
    response = client.get('/entry/5')
    assert response.status_code == 404


@pytest.mark.parametrize(
    'path',
    (
        '/edit/create',
        '/edit/update/1',
        '/edit/delete/1',
    )
)
def test_login_required_post(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize(
    'path',
    ('/edit/update/5', '/edit/delete/5')
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_list_for_editors(client, auth):
    response = client.get('/edit/')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    auth.login()
    response = client.get('/edit/')
    assert response.status_code == 200
    assert b'Test Title 1' in response.data
    assert b'2019-01-01' in response.data

def test_create(client, auth, app):
    auth.login()
    assert client.get('/edit/create').status_code == 200

    title = 'created'
    body = 'created on test'
    client.post(
        '/edit/create',
        data={'title': title, 'body': body}
    )

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 4')
            entry = cursor.fetchone()
        assert entry['author_id'] == 1
        assert entry['title'] == title
        assert entry['body'] == body


def test_update(client, auth, app):
    entry_id = 1
    title = 'updated'
    body = 'updated on test'
    url = '/edit/update/{0}'.format(entry_id)

    auth.login()
    assert client.get(url).status_code == 200
    client.post(
        url,
        data={'title': title, 'body': body}
    )

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
    ('/edit/create', '/edit/update/1')
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    entry_id = 1
    auth.login()
    response = client.post('/edit/delete/{0}'.format(entry_id))
    assert response.headers['Location'] == 'http://localhost/edit/'

    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM entry WHERE id = %s',
                (entry_id,)
            )
            entry = cursor.fetchone()
        assert entry is None
