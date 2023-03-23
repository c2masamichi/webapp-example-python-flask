import pytest

from werkzeug.security import generate_password_hash

from cms.database import db
from cms.models import User


def test_fetch_all(app):
    with app.app_context():
        users = User.query.all()
        assert len(users) == 3


def test_fetch(app):
    user_id = 1
    role = 'administrator'
    name = 'user-admin01'

    with app.app_context():
        user = User.query.get(user_id)
        assert user.id == user_id
        assert user.name == name
        assert user.role == role


def test_create(app):
    role = 'administrator'
    name = 'added-user_01'
    password = 'ab-cd_1234'

    with app.app_context():
        user = User(
            role=role, name=name,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        assert user.id == 4


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


def test_update(app):
    user_id = 2
    role = 'author'
    name = 'updated-to-author02'

    with app.app_context():
        user = User.query.get(user_id)
        user.role = role
        user.name = name
        db.session.commit()


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


def test_delete(app):
    user_id = 2
    with app.app_context():
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
