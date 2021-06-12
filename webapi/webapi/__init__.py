import os
import sys

from flask import Flask

from webapi.models import Product


CONFIGS = {
    'production': 'config-production.py',
    'development': 'config-development.py',
    'testing': 'config-testing.py',
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
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
            app.config['DB_USER'],
            app.config['DB_PASSWORD'],
            app.config['DB_HOST'],
            app.config['DB_PORT'],
            app.config['DATABASE'],
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from webapi import error_handler as eh

    app.register_error_handler(400, eh.bad_request)
    app.register_error_handler(404, eh.not_found)
    app.register_error_handler(500, eh.internal_server_error)

    from webapi.database import init_app
    from webapi.cli import add_cli

    init_app(app)
    add_cli(app)

    from webapi import api

    app.register_blueprint(api.bp)

    return app
