import pytest

from cms.user_wrappers import auth_user


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
