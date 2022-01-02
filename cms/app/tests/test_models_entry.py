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
    with app.app_context():
        with pytest.raises(AssertionError):
            author_id = 1
            Entry(title=title, body=body, author_id=author_id)


@pytest.mark.parametrize(
    ('title', 'body'),
    (
        ('a' * 101, 'updated on test'),
        ('updated on test', 'a' * 10001),
    ),
)
def test_update_validate(app, title, body):
    with app.app_context():
        with pytest.raises(AssertionError):
            entry_id = 1
            entry = Entry.query.get(entry_id)
            entry.title = title
            entry.body = body