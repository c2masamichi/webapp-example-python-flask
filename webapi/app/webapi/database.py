import time

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def init_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()
