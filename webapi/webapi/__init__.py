import os
import sys

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError:
        print('[Error] instance/config.py must exist.', file=sys.stderr)
        sys.exit(1)

    @app.route('/healthcheck')
    def healthcheck():
        return 'app running'

    from webapi import db

    db.init_app(app)

    from webapi import api

    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='index')

    return app
