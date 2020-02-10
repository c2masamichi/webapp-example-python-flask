from datetime import datetime

from cms.db import get_db
from cms.model import Entry


def test_fetch_all(app):
    with app.app_context():
        result = Entry().fetch_all()
        assert result.succeeded

        entries = result.value
        assert len(entries) == 3

        # sorted by created desc
        assert entries[0]['created'] == datetime(2019, 1, 2, 8, 20, 1)
        assert entries[1]['created'] == datetime(2019, 1, 1, 12, 30, 45)
        assert entries[2]['created'] == datetime(2019, 1, 1, 0, 0, 0)


def test_fetch(app):
    with app.app_context():
        entry_id = 1
        result = Entry().fetch(entry_id)
        assert result.succeeded

        entry = result.value
        assert entry['id'] == 1
        assert entry['title'] == 'Test Title 1'
        assert entry['body'] == 'This body is test.'
        assert entry['created'] == datetime(2019, 1, 1, 0, 0)


def test_fetch_not_exists(app):
    with app.app_context():
        entry_id = 5
        result = Entry().fetch(entry_id)
        assert result.succeeded

        entry = result.value
        assert entry is None


def test_create(app):
    with app.app_context():
        title = 'created'
        body = 'created on test'
        result = Entry().create(title, body)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 4')
            entry = cursor.fetchone()
        assert entry['title'] == 'created'
        assert entry['body'] == 'created on test'


def test_update(app):
    with app.app_context():
        entry_id = 1
        title = 'updated'
        body = 'updated on test'
        result = Entry().update(entry_id, title, body)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 1')
            entry = cursor.fetchone()
        assert entry['title'] == 'updated'
        assert entry['body'] == 'updated on test'


def test_delete(app):
    with app.app_context():
        entry_id = 1
        result = Entry().delete(entry_id)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 1')
            entry = cursor.fetchone()
        assert entry is None
