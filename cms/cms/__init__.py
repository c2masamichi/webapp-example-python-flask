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

    from cms import db

    db.init_app(app)

    from cms import auth, blog, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    return app
