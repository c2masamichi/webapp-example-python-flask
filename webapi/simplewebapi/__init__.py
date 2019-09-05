import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'webapi.sqlite'),
    )

    @app.route('/healthcheck')
    def healthcheck():
        return 'app running'

    from simplewebapi import db

    db.init_app(app)

    from simplewebapi import api

    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='index')

    return app
