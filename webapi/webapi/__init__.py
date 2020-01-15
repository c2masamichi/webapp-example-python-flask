import os
import sys

from flask import Flask


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

    @app.route('/healthcheck')
    def healthcheck():
        return 'app running'

    from webapi import error_handler as eh

    app.register_error_handler(404, eh.not_found)

    from webapi import db

    db.init_app(app)

    from webapi import api

    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='index')

    return app
