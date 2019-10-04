import os
import tempfile

import pytest
from cms import create_app
from cms.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(
        {
            'TESTING': True,
            'SECRET_KEY': 'test',
            'DATABASE': db_path
        }
    )

    with app.app_context():
        file_path = os.path.join(os.path.dirname(__file__), 'data.sql')
        init_db(file_path)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='testuser', password='testpass'):
        return self._client.post(
            '/auth/login', data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
