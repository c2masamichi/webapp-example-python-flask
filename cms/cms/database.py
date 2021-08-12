import time

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def init_db(num_retries=2, retry_interval=5):
    for retry in range(num_retries + 1):
        try:
            db.drop_all(app=current_app)
            db.create_all(app=current_app)
        except OperationalError as err:
            current_app.logger.error(
                'sqlalchemy.exc.OperationalError: {0}'.format(err))
            current_app.logger.error(
                'retrying operation: {0}'.format(retry + 1))
            if retry >= num_retries:
                raise Exception('over num_retries') from None
            time.sleep(retry_interval)
        else:
            break
