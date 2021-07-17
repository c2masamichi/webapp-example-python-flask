import pytest

from cms.user_wrappers import auth_user


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
