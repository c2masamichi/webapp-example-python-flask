import os
import sys

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'cms.sqlite'),
    )

    if test_config is None:
        try:
            app.config.from_pyfile('config.py')
        except FileNotFoundError:
            print('[Error] instance/config.py must exist.', file=sys.stderr)
            sys.exit(1)
    else:
        app.config.update(test_config)

    @app.route('/healthcheck')
    def healthcheck():
        return 'app running'

    from cms import db

    db.init_app(app)

    from cms import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
