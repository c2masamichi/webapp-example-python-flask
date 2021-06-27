from datetime import datetime
import re

from sqlalchemy.orm import validates

from cms.database import db
from cms.role import ROLE_PRIV


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)


    @validates('role')
    def validate_role(self, key, user):
        assert user in ROLE_PRIV
        return user

    @validates('name')
    def validate_name(self, key, user):
        max_length = 20
        pattern = r'[0-9a-zA-Z-_]*'

        assert len(user) <= max_length
        assert re.fullmatch(pattern, user) is not None
        return user


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    body = db.Column(db.String(10000), unique=True, nullable=False)
    created = db.Column(db.DataTime, nullable=False,
        default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @validates('title')
    def validate_title(self, key, entry):
        max_length = 100
        assert len(entry) <= max_length
        return entry

    @validates('body')
    def validate_body(self, key, entry):
        max_length = 10000
        assert len(entry) <= max_length
        return entry
