import pytest

from webapi import create_app
from webapi.db import close_db
from webapi.db import get_db
from webapi.db import init_db


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        init_db(withdata=True)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
