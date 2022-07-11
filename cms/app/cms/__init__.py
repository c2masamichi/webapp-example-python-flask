import os
import sys

from flask import Flask

from cms.models import Entry
from cms.models import User


CONFIGS = {
    'production': 'config-production.py',
    'development': 'config-development.py',
}


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_name = CONFIGS[os.getenv('FLASK_ENV', 'production')]

    try:
        app.config.from_pyfile(config_name)
        app.logger.info('config file successfully loaeded.')
    except FileNotFoundError:
        app.logger.error('config file must exist.')
        sys.exit(1)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}'.format(
            app.config['DB_USER'],
            app.config['DB_PASSWORD'],
            app.config['DB_HOST'],
            app.config['DB_PORT'],
            app.config['DATABASE'],
            'utf8mb4',
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from cms import error_handler as eh

    app.register_error_handler(404, eh.not_found)

    from cms.database import init_app
    from cms.cli import add_cli

    init_app(app)
    add_cli(app)

    from cms import auth, blog, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    return app
