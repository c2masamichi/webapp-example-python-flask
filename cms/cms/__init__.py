import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'cms.sqlite'),
    )

    if test_config is not None:
        app.config.update(test_config)

    @app.route('/healthcheck')
    def healthcheck():
        return 'app running'

    return app
