from datetime import datetime
import re

from sqlalchemy.orm import validates

from cms.database import db
from cms.role import ROLE_PRIV


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    body = db.Column(db.String(10000), unique=True, nullable=False)
    created = db.Column(db.DataTime, nullable=False,
        default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

