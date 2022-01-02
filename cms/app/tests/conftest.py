import pytest

from cms import create_app
from cms.database import init_db
from cms.utils import load_data


@pytest.fixture
def app():
    new_app = create_app()

    with new_app.app_context():
        init_db()
        load_data()

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
