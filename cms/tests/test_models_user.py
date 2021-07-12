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
        ('author', 'user-a_01%', 'ef-gh_5678'),
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
