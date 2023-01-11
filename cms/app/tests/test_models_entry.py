import pytest

from cms.models import Entry


@pytest.mark.parametrize(
    ('title', 'body'),
    (
        ('a' * 101, 'created on test'),
        ('created on test', 'a' * 10001),
    ),
)
def test_create_validate(app, title, body):
    author_id = 1
    with app.app_context():
        with pytest.raises(AssertionError):
            Entry(title=title, body=body, author_id=author_id)


@pytest.mark.parametrize(
    ('title', 'body'),
    (
        ('a' * 101, 'updated on test'),
        ('updated on test', 'a' * 10001),
    ),
)
def test_update_validate(app, title, body):
    entry_id = 1
    with app.app_context():
        with pytest.raises(AssertionError):
            entry = Entry.query.get(entry_id)
            entry.title = title
            entry.body = body