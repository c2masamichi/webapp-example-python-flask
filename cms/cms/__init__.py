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

    from cms import db

    db.init_app(app)

    from cms import auth, blog, mypage, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(mypage.bp)
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    return app
