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
        username = 'added-user_01'
        password = 'ab-cd_1234'
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
    ('role', 'username', 'password', 'message'),
    (
        ('aaa', 'user-a_01', 'ef-gh_5678', 'does not exist'),
        ('author', 'a' * 21, 'ef-gh_5678', 'Bad data'),
        ('author', 'user-a_01', 'a' * 31, 'Bad data'),
        ('author', 'user-author01', 'efgh5678', 'already registered'),
    ),
)
def test_create_validate(app, role, username, password, message):
    with app.app_context():
        result = User().create(role, username, password)
        assert not result.succeeded
        assert message in result.description


def test_update(app):
    with app.app_context():
        user_id = 2
        role = 'author'
        username = 'updated-to-author02'
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
        ('aaa', 'user-a_01', 'does not exist'),
        ('author', 'a' * 21, 'Bad data'),
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
        user_id = 2
        username = 'user-editor01'
        new_password = 'updated-pass_01'
        result = User().change_password(
            user_id, new_password, old_required=False)
        assert result.succeeded

        auth_result = User().auth(username, new_password)
        assert auth_result.succeeded


def test_change_own_password(app):
    with app.app_context():
        user_id = 1
        username = 'user-admin01'
        old_password = 'testpass'
        new_password = 'updated-pass_01'
        result = User().change_password(user_id, new_password, old_password)
        assert result.succeeded

        auth_result = User().auth(username, old_password)
        assert not auth_result.succeeded

        auth_result = User().auth(username, new_password)
        assert auth_result.succeeded


def test_change_password_validate01(app):
    with app.app_context():
        user_id = 1
        new_password = 'updated-pass_01'
        result = User().change_password(user_id, new_password)
        assert not result.succeeded


def test_change_password_validate02(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'
        new_password = 'updated-pass_01'
        result = User().change_password(user_id, new_password, old_password)
        assert not result.succeeded
