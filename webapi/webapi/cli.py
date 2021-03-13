import click
from flask.cli import with_appcontext

from webapi.db import init_db
from webapi.db import load_data


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


@click.command('load-data')
@with_appcontext
def load_data_command():
    load_data()
    click.echo('Loaded data.')


def add_cli(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)
