from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/test')
    def hello_world():
        return 'app running'

    from simplewebapi import api

    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='index')

    return app
