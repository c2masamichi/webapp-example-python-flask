import pytest

from cms import create_app
from cms.db import init_db


@pytest.fixture
def app():
    new_app = create_app()

    with new_app.app_context():
        init_db(withdata=True)

    yield new_app


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, role='administrator'):
        role_user = {
            'administrator': 'user-admin01',
            'editor': 'user-editor01',
            'author': 'user-author01',
        }

        username = role_user[role]
        password = 'testpass'
        return self._client.post(
            '/admin/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
