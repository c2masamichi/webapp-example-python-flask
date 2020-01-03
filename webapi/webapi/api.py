from flask import Blueprint
from flask import jsonify
from flask import request

from webapi.model import Product

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return 'top'


@bp.route('/products')
def get_products():
    result = Product().fetch_all()
    return jsonify(result)


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    result = Product().fetch(product_id)
    if result is None:
        error = {
            'error': 'Not Found.'
        }
        return jsonify(error), 404
    return jsonify(result)


@bp.route('/products', methods=['POST'])
def create_product():
    if request.headers.get('Content-Type') != 'application/json':
        error = {
            'error': 'Content-Type must be application/json.'
        }
        return jsonify(error), 400

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    error_msg = ''
    if name is None or price is None:
        error = {
            'error': 'The key "name" and "price" are required.'
        }
        return jsonify(error), 400

    result = Product().create(name, price)
    return jsonify(result), 201


@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if request.headers.get('Content-Type') != 'application/json':
        error = {
            'error': 'Content-Type must be application/json.'
        }
        return jsonify(error), 400

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    error_msg = ''
    if name is None or price is None:
        error = {
            'error': 'The key "name" and "price" are required.'
        }
        return jsonify(error), 400

    product = Product().fetch(product_id)
    if product is None:
        error = {
            'error': 'Not Found.'
        }
        return jsonify(error), 404

    result = Product().update(product_id, name, price)
    return jsonify(result)


@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product().fetch(product_id)
    if product is None:
        error = {
            'error': 'Not Found.'
        }
        return jsonify(error), 404

    result = Product().delete(product_id)
    return jsonify(result)
