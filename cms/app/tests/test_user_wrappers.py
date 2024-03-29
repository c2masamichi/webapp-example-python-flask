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
def test_auth_user_incorrect_name_or_password(app, name, password):
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


def test_change_password_validate_missing_old_password(app):
    with app.app_context():
        user_id = 1
        new_password = 'updated-pass_01'
        # Default: old_required=True
        succeeded, message = change_password(
            user_id, new_password)  # missing old password
        assert not succeeded
        assert 'Incorrect password.' in message


def test_change_password_validate_incorrect_password(app):
    with app.app_context():
        user_id = 1
        old_password = 'aaaa'  # incorrect password
        new_password = 'updated-pass_01'
        succeeded, message = change_password(
            user_id, new_password, old_password)
        assert not succeeded
        assert 'Incorrect password.' in message


@pytest.mark.parametrize(
    'new_password',
    (
        'a' * 7,
        'a' * 31,
        'ef-gh_5678%',
    ),
)
def test_change_password_validate_new_password(app, new_password):
    with app.app_context():
        user_id = 2
        succeeded, message = change_password(
            user_id, new_password, old_required=False)
        assert not succeeded
        assert 'Bad data' in message


def test_change_password_validate04(app):
    with app.app_context():
        user_id = 10
        new_password = 'updated-pass_01'
        succeeded, message = change_password(
            user_id, new_password, old_required=False)
        assert not succeeded
        assert 'Update failed.' in message
