from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/product/<int:product_id>')
    def get_product(product_id):
        return 'get {0}'.format(product_id)

    return app
