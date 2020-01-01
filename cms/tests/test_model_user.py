import pytest

from cms.db import get_db
from cms.model import User


def test_fetch_all(app):
    with app.app_context():
        users = User().fetch_all()
        assert len(users) == 1


def test_fetch(app):
    with app.app_context():
        user_id = 1
        user = User().fetch(user_id)
        assert user['id'] == 1
        assert user['username'] == 'testuser'


def test_fetch_not_exists(app):
    with app.app_context():
        user_id = 5
        user = User().fetch(user_id)
        assert user is None


def test_auth(app):
    with app.app_context():
        username = 'testuser'
        password = 'testpass'
        user, error = User().auth(username, password)
        assert error is None
        assert user['id'] == 1
        assert user['username'] == 'testuser'


@pytest.mark.parametrize(
    ('username', 'password'),
    (
        ('aaaa', 'testpass'),
        ('testuser', 'aaaa')
    ),
)
def test_auth_error(app, username, password):
    with app.app_context():
        user, error = User().auth(username, password)
        assert error == 'Incorrect username or password.'
        assert user is None


def test_create(app):
    with app.app_context():
        username = 'addeduser'
        password = 'abcd1234'
        error = User().create(username, password)
        assert error is None

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where username = %s',
                (username,)
            )
            user = cursor.fetchone()
        assert user is not None


def test_create_error(app):
    with app.app_context():
        username = 'testuser'
        password = 'efgh5678'
        error = User().create(username, password)
        assert 'already registered' in error


def test_delete(app):
    with app.app_context():
        user_id = 1
        User().delete(user_id)

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert user is None


def test_change_password(app):
    with app.app_context():
        user_id = 1
        username = 'testuser'
        old_password = 'testpass'
        new_password = 'updated'
        error = User().change_password(user_id, old_password, new_password)
        assert error is None

        user, error = User().auth(username, old_password)
        assert error is not None

        user, error = User().auth(username, new_password)
        assert error is None
        assert user['id'] == 1


def test_change_password_error(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'
        new_password = 'updated'
        error = User().change_password(user_id, old_password, new_password)
        assert error == 'Incorrect password.'