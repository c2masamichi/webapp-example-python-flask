import pytest

from werkzeug.security import generate_password_hash

from cms.database import db
from cms.models import User


@pytest.mark.parametrize(
    ('role', 'name', 'password'),
    (
        ('aaa', 'user-a_01', 'ef-gh_5678'),
        ('author', 'a' * 3, 'ef-gh_5678'),
        ('author', 'a' * 21, 'ef-gh_5678'),
        ('author', 'user-a_01%', 'ef-gh_5678'),
    ),
)
def test_create_validate(app, role, name, password):
    with app.app_context():
        with pytest.raises(AssertionError):
            User(
                role=role, name=name,
                password=generate_password_hash(password)
            )


@pytest.mark.parametrize(
    ('role', 'name'),
    (
        ('aaa', 'user-a_01'),
        ('author', 'a' * 3),
        ('author', 'a' * 21),
        ('author', 'user-a_01%'),
    ),
)
def test_update_validate(app, role, name):
    user_id = 2
    with app.app_context():
        user = db.session.get(User, user_id)
        with pytest.raises(AssertionError):
            user.role = role
            user.name = name
