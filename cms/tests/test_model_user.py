import pytest

from cms.db import get_db
from cms.model import User


def test_fetch_all(app):
    with app.app_context():
        result = User().fetch_all()
        assert result.succeeded

        users = result.value
        assert len(users) == 3


def test_fetch(app):
    with app.app_context():
        user_id = 1
        role = 'administrator'
        username = 'user-admin01'
        result = User().fetch(user_id)
        assert result.succeeded

        user = result.value
        assert user['id'] == user_id
        assert user['username'] == username
        assert user['role'] == role


def test_fetch_not_exists(app):
    with app.app_context():
        user_id = 5
        result = User().fetch(user_id)
        assert result.succeeded

        user = result.value
        assert user is None


def test_auth(app):
    with app.app_context():
        username = 'user-admin01'
        password = 'testpass'
        result = User().auth(username, password)
        assert result.succeeded

        user = result.value
        assert user['id'] == 1
        assert user['username'] == username


@pytest.mark.parametrize(
    ('username', 'password'),
    (
        ('aaaa', 'testpass'),
        ('user-admin01', 'aaaa')
    ),
)
def test_auth_validate(app, username, password):
    with app.app_context():
        result = User().auth(username, password)
        assert not result.succeeded

        user = result.value
        assert user is None


def test_create(app):
    with app.app_context():
        role = 'administrator'
        username = 'addeduser'
        password = 'abcd1234'
        result = User().create(role, username, password)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where username = %s',
                (username,)
            )
            user = cursor.fetchone()
        assert user is not None


@pytest.mark.parametrize(
    ('role', 'username', 'message'),
    (
        ('aaa', 'addeduser', 'does not exist'),
        ('author', 'user-author01', 'already registered'),
    ),
)
def test_create_validate(app, role, username, message):
    with app.app_context():
        password = 'efgh5678'
        result = User().create(role, username, password)
        assert not result.succeeded
        assert message in result.description


def test_update(app):
    with app.app_context():
        user_id = 2
        role = 'author'
        username = 'updated-to-author'
        result = User().update(user_id, role, username)
        assert result.succeeded

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'select * from user where id = %s',
                (user_id,)
            )
            user = cursor.fetchone()
        assert user['role'] == role
        assert user['username'] == username


@pytest.mark.parametrize(
    ('role', 'username', 'message'),
    (
        ('aaa', 'addeduser', 'does not exist'),
        ('author', 'user-author01', 'already registered'),
    ),
)
def test_update_validate(app, role, username, message):
    with app.app_context():
        user_id = 2
        result = User().update(user_id, role, username)
        assert not result.succeeded
        assert message in result.description


def test_delete(app):
    with app.app_context():
        user_id = 2
        result = User().delete(user_id)
        assert result.succeeded

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
        username = 'user-admin01'
        old_password = 'testpass'
        new_password = 'updated'
        result = User().change_password(user_id, old_password, new_password)
        assert result.succeeded

        auth_result = User().auth(username, old_password)
        assert not auth_result.succeeded

        auth_result = User().auth(username, new_password)
        assert auth_result.succeeded
        user = auth_result.value
        assert user['id'] == user_id


def test_change_password_validate(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'
        new_password = 'updated'
        result = User().change_password(user_id, old_password, new_password)
        assert not result.succeeded
