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
