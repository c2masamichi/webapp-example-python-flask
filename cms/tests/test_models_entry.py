from datetime import datetime

from cms.db import get_db
from cms.models import Entry


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
        assert entry['id'] == entry_id
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
        author_id = 1
        title = 'created'
        body = 'created on test'
        result = Entry().create(author_id, title, body)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM entry WHERE id = 4')
            entry = cursor.fetchone()
        assert entry['author_id'] == author_id
        assert entry['title'] == title
        assert entry['body'] == body


def test_create_validate(app):
    with app.app_context():
        author_id = 1
        title = 'a' * 101
        body = 'created on test'
        message = 'Bad data'
        result = Entry().create(author_id, title, body)
        assert not result.succeeded
        assert message in result.description


def test_update(app):
    with app.app_context():
        entry_id = 1
        title = 'updated'
        body = 'updated on test'
        result = Entry().update(entry_id, title, body)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM entry WHERE id = %s',
                (entry_id,)
            )
            entry = cursor.fetchone()
        assert entry['title'] == title
        assert entry['body'] == body


def test_update_validate(app):
    with app.app_context():
        entry_id = 1
        title = 'a' * 101
        body = 'updated on test'
        message = 'Bad data'
        result = Entry().update(entry_id, title, body)
        assert not result.succeeded
        assert message in result.description


def test_delete(app):
    with app.app_context():
        entry_id = 1
        result = Entry().delete(entry_id)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM entry WHERE id = %s',
                (entry_id,)
            )
            entry = cursor.fetchone()
        assert entry is None
