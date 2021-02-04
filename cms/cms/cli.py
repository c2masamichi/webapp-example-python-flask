import click
from flask.cli import with_appcontext

from cms.model import User


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
