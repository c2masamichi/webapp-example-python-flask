from datetime import datetime

import pytest

from cms.database import db
from cms.models import Entry


def test_fetch_all(app):
    with app.app_context():
        entries = Entry.query.all()
        assert len(entries) == 3

        # sorted by created desc
        assert entries[0]['created'] == datetime(2019, 1, 2, 8, 20, 1)
        assert entries[1]['created'] == datetime(2019, 1, 1, 12, 30, 45)
        assert entries[2]['created'] == datetime(2019, 1, 1, 0, 0, 0)


def test_fetch(app):
    with app.app_context():
        entry_id = 1
        entry = Entry.query.get(entry_id)
        assert entry.id == entry_id
        assert entry.title == 'Test Title 1'
        assert entry.body == 'This body is test.'
        assert entry.created == datetime(2019, 1, 1, 0, 0)


def test_create(app):
    with app.app_context():
        author_id = 1
        title = 'created'
        body = 'created on test'
        entry = Entry(title=title, body=body, author_id=author_id)
        db.session.add(entry)
        db.session.commit()
        assert entry.id == 4


def test_create_validate(app):
    with app.app_context():
        with pytest.raises(AssertionError):
            author_id = 1
            title = 'a' * 101
            body = 'created on test'
            Entry(title=title, body=body, author_id=author_id)


def test_update(app):
    with app.app_context():
        entry_id = 1
        title = 'updated'
        body = 'updated on test'
        entry = Entry.query.get(entry_id)
        entry.title = title
        entry.body = body
        db.session.commit()


def test_update_validate(app):
    with app.app_context():
        with pytest.raises(AssertionError):
            entry_id = 1
            title = 'a' * 101
            body = 'updated on test'
            entry = Entry.query.get(entry_id)
            entry.title = title
            entry.body = body


def test_delete(app):
    with app.app_context():
        entry_id = 1
        entry = Entry.query.get(entry_id)
        db.session.delete(entry)
        db.session.commit()
