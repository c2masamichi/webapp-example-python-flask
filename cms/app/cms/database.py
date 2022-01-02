import time

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def init_db():
    db.drop_all(app=current_app)
    db.create_all(app=current_app)
