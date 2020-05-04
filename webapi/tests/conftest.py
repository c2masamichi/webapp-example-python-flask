import pytest

from webapi import create_app
from webapi.db import init_db


@pytest.fixture
def app():
    new_app = create_app()

    with new_app.app_context():
        init_db(withdata=True)

    yield new_app


@pytest.fixture
def client(app):
    return app.test_client()
