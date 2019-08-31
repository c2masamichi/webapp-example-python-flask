import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JSON_PATH=os.path.join(app.instance_path, 'data.json'),
    )

    @app.route('/test')
    def hello_world():
        return 'app running'

    from simplewebapi import api

    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='index')

    return app
