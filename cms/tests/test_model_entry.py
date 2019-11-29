from datetime import datetime

from cms.db import get_db
from cms.model import Entry


def test_fetch_all(app):
    with app.app_context():
        entries = Entry().fetch_all()
        assert len(entries) == 3
        # sorted by created desc
        assert entries[0]['created'] == datetime(2019, 1, 2, 8, 20, 1)
        assert entries[1]['created'] == datetime(2019, 1, 1, 12, 30, 45)
        assert entries[2]['created'] == datetime(2019, 1, 1, 0, 0, 0)


def test_fetch(app):
    with app.app_context():
        entry_id = 1
        entry = Entry().fetch(entry_id)
        assert entry['id'] == 1
        assert entry['title'] == 'Test Title 1'
        assert entry['body'] == 'This body is test.'
        assert entry['created'] == datetime(2019, 1, 1, 0, 0)

def test_fetch_not_exists(app):
    with app.app_context():
        entry_id = 5
        entry = Entry().fetch(entry_id)
        assert entry is None
