import pytest
from werkzeug.security import check_password_hash

from cms.db import get_db


@pytest.mark.parametrize(
    'path',
    (
        '/mypage/',
        '/admin/password_change/',
    )
)
def test_login_required_get(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/admin/login'


def test_list_for_editors(client, auth):
    auth.login()
    response = client.get('/mypage/')
    assert response.status_code == 200
    assert b'user-admin01' in response.data
    assert b'administrator' in response.data


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
