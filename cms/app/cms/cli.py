import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from cms.database import db
from cms.database import init_db
from cms.models import User
from cms.user_wrappers import validate_password
from cms.utils import load_data


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
    if not validate_password(password):
        click.echo('[Error]: Passsword is invalid')
    elif User.query.filter_by(name=username).first() is not None:
        click.echo('[Error]: User {0} is already registered.'.format(username))
    else:
        try:
            user = User(
                role='administrator', name=username,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
        except AssertionError:
            click.echo('[Error]: AssertionError')
        else:
            click.echo('Created the superuser.')


def add_cli(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)
    app.cli.add_command(create_superuser)
