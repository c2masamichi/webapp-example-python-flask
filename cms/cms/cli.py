import click
from flask.cli import with_appcontext

from cms.db import init_db
from cms.model import User


@click.command('init-db')
@click.option('--withdata', is_flag=True)
@with_appcontext
def init_db_command(withdata):
    init_db(withdata)
    click.echo('Initialized the database.')


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
    app.cli.add_command(create_superuser)
