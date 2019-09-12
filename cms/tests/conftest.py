import os
import tempfile

import pytest
from cms import create_app
from cms.db import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context():
        file_path = os.path.join(os.path.dirname(__file__), 'data.sql')
        init_db(file_path)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
