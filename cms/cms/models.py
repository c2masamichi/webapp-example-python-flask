from datetime import datetime
import re

from sqlalchemy.orm import validates

from cms.database import db
from cms.role import ROLE_PRIV


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)

    @validates('role')
    def validate_role(self, key, role):
        assert role in ROLE_PRIV
        return role

    @validates('name')
    def validate_name(self, key, name):
        max_length = 20
        pattern = r'[0-9a-zA-Z-_]*'

        assert len(name) <= max_length
        assert re.fullmatch(pattern, name) is not None
        return name


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @validates('title')
    def validate_title(self, key, title):
        max_length = 100
        assert len(title) <= max_length
        return title

    @validates('body')
    def validate_body(self, key, body):
        max_length = 10000
        assert len(body) <= max_length
        return body
