import pytest

from webapi import create_app
from webapi.database import init_db
from webapi.utils import load_data


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
