from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from webapi.model import Product

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return 'top'


@bp.route('/products')
def get_products():
    result = Product().fetch_all()
    if result.code != 200:
        abort(result.code, description=result.description)
    return jsonify(result.value)


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    result = fetch_product_wrapper(product_id)
    return jsonify(result.value)


@bp.route('/products', methods=['POST'])
def create_product():
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, description='Content-Type must be application/json.')

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    error_msg = ''
    if name is None or price is None:
        abort(400, description='The key "name" and "price" are required.')

    result = Product().create(name, price)
    if result.code != 200:
        abort(result.code, description=result.description)
    return jsonify(result.value)


@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, description='Content-Type must be application/json.')

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if name is None or price is None:
        abort(400, description='The key "name" and "price" are required.')

    fetch_product_wrapper(product_id)

    result = Product().update(product_id, name, price)
    if result.code != 200:
        abort(result.code, description=result.description)
    return jsonify(result.value)


@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    fetch_product_wrapper(product_id)

    result = Product().delete(product_id)
    if result.code != 200:
        abort(result.code, description=result.description)
    return jsonify(result.value)


def fetch_product_wrapper(product_id):
    result = Product().fetch(product_id)
    if result.code != 200:
        abort(result.code, description=result.description)
    if not result.value:
        abort(404, description='product {0}'.format(product_id))
    return result
