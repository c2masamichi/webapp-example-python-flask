import pytest

from cms.database import db
from cms.models import User


def test_fetch_all(app):
    with app.app_context():
        users = User.query.all()
        assert len(users) == 3


def test_fetch(app):
    with app.app_context():
        user_id = 1
        role = 'administrator'
        name = 'user-admin01'
        user = User.query.get(user_id)
        assert user.id == user_id
        assert user.name == name
        assert user.role == role


def test_auth(app):
    with app.app_context():
        name = 'user-admin01'
        password = 'testpass'
        result = User.auth(name, password)
        assert result.succeeded

        user = result.value
        assert user.id == 1
        assert user.name == name


@pytest.mark.parametrize(
    ('name', 'password'),
    (
        ('aaaa', 'testpass'),
        ('user-admin01', 'aaaa')
    ),
)
def test_auth_validate(app, name, password):
    with app.app_context():
        result = User.auth(name, password)
        assert not result.succeeded

        user = result.value
        assert user is None


def test_create(app):
    with app.app_context():
        role = 'administrator'
        name = 'added-user_01'
        password = 'ab-cd_1234'
        user = User.create(role=role, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        assert user.id == 4


@pytest.mark.parametrize(
    ('role', 'name', 'password'),
    (
        ('aaa', 'user-a_01', 'ef-gh_5678'),
        ('author', 'a' * 21, 'ef-gh_5678'),
        ('author', 'user-a_01', 'a' * 31),
        ('author', 'user-a_01%', 'ef-gh_5678'),
        ('author', 'user-a_01', 'ef-gh_5678%'),
        ('author', 'user-author01', 'efgh5678'),
    ),
)
def test_create_validate(app, role, name, password):
    with app.app_context():
        with pytest.raises(AssertionError):
            User.create(role=role, name=name, password=password)


def test_update(app):
    with app.app_context():
        user_id = 2
        role = 'author'
        name = 'updated-to-author02'
        user = User.query.get(user_id)
        user.role = role
        user.name = name


@pytest.mark.parametrize(
    ('role', 'name'),
    (
        ('aaa', 'user-a_01'),
        ('author', 'a' * 21),
        ('author', 'user-a_01%'),
        ('author', 'user-author01'),
    ),
)
def test_update_validate(app, role, name):
    with app.app_context():
        with pytest.raises(AssertionError):
            user_id = 2
            user = User.query.get(user_id)
            user.role = role
            user.name = name


def test_delete(app):
    with app.app_context():
        user_id = 2
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()


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
        message = 'Incorrect password.'
        # Default: old_required=True
        result = User().change_password(user_id, new_password)
        assert not result.succeeded
        assert message in result.description


def test_change_password_validate02(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'
        new_password = 'updated-pass_01'
        message = 'Incorrect password.'
        result = User().change_password(user_id, new_password, old_password)
        assert not result.succeeded
        assert message in result.description


@pytest.mark.parametrize(
    ('new_password', 'message'),
    (
        ('a' * 31, 'Bad data'),
        ('ef-gh_5678%', 'Bad data'),
    ),
)
def test_change_password_validate03(app, new_password, message):
    with app.app_context():
        user_id = 2
        result = User().change_password(
            user_id, new_password, old_required=False)
        assert not result.succeeded
        assert message in result.description
