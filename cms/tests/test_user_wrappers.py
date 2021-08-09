import pytest

from cms.user_wrappers import auth_user
from cms.user_wrappers import change_password


def test_auth(app):
    with app.app_context():
        name = 'user-admin01'
        password = 'testpass'
        user = auth_user(name, password)
        assert user.id == 1
        assert user.name == name


@pytest.mark.parametrize(
    ('name', 'password'),
    (
        ('aaaa', 'testpass'),
        ('user-admin01', 'aaaa')
    ),
)
def test_auth_user_validate(app, name, password):
    with app.app_context():
        user = auth_user(name, password)
        assert user is None


def test_change_password(app):
    with app.app_context():
        user_id = 2
        name = 'user-editor01'
        new_password = 'updated-pass_01'
        succeeded, message = change_password(
            user_id, new_password, old_required=False)
        assert succeeded
        assert 'Password Changed.' in message

        user = auth_user(name, new_password)
        assert user is not None


def test_change_own_password(app):
    with app.app_context():
        user_id = 1
        name = 'user-admin01'
        old_password = 'testpass'
        new_password = 'updated-pass_01'
        succeeded, message = change_password(
            user_id, new_password, old_password)
        assert succeeded
        assert 'Password Changed.' in message

        user = auth_user(name, old_password)
        assert user is None

        user = auth_user(name, new_password)
        assert user is not None


def test_change_password_validate01(app):
    with app.app_context():
        user_id = 1
        new_password = 'updated-pass_01'
        # Default: old_required=True
        succeeded, message = change_password(
            user_id, new_password)
        assert not succeeded
        assert 'Incorrect password.' in message


def test_change_password_validate02(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'
        new_password = 'updated-pass_01'
        succeeded, message = change_password(
            user_id, new_password, old_password)
        assert not succeeded
        assert 'Incorrect password.' in message


@pytest.mark.parametrize(
    ('new_password', 'err_msg'),
    (
        ('a' * 31, 'Bad data'),
        ('ef-gh_5678%', 'Bad data'),
    ),
)
def test_change_password_validate03(app, new_password, err_msg):
    with app.app_context():
        user_id = 2
        succeeded, message = change_password(
            user_id, new_password, old_required=False)
        assert not succeeded
        assert err_msg in message