import click
from flask.cli import with_appcontext

from cms.db import init_db
from cms.db import load_data
from cms.models import User


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


@click.command('create-superuser')
@click.option('--username', required=True)
@click.password_option()
@with_appcontext
def create_superuser(username, password):
    result = User().create('administrator', username, password)
    if result.succeeded:
        click.echo('Created the superuser.')
    else:
        click.echo('[Error]: {0}'.format(result.description))


def add_cli(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)
    app.cli.add_command(create_superuser)
