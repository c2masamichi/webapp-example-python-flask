import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import pymysql

from webapi.schema import SCHEMA_STATEMENTS
from tests.data import TEST_DATA_STATEMENTS


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            db=current_app.config['DATABASE'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(withdata):
    db = get_db()
    with db.cursor() as cursor:
        for statement in SCHEMA_STATEMENTS:
            cursor.execute(statement)
    db.commit()

    if withdata:
        with db.cursor() as cursor:
            for statement in TEST_DATA_STATEMENTS:
                cursor.execute(statement)
        db.commit()


@click.command('init-db')
@click.option('--withdata', is_flag=True)
@with_appcontext
def init_db_command(withdata):
    init_db(withdata)
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
