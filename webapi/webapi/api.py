from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from webapi.models import Product

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/products')
def get_products():
    """Fetch products.

    Returns:
        str: json
    """
    result = Product().fetch_all()
    if result.code != 200:
        abort(result.code, description=result.description)

    data = {
        'result': [
            {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
            }
            for product in result.value
        ]
    }
    return jsonify(data)


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    """Fetch product.

    Args:
        product_id (int): id of product to fetch

    Returns:
        str: json
    """
    result = fetch_product_wrapper(product_id)
    product = result.value
    data = {
        'result': {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
        }
    }
    return jsonify(data)


@bp.route('/products', methods=['POST'])
def create_product():
    """Create product.

    Args:
        name (str): name of product
        price (int): price of product

    Returns:
        str: json
    """
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, description='Content-Type must be application/json.')

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if name is None or price is None:
        abort(400, description='The key "name" and "price" are required.')

    result = Product().create(name, price)
    if result.code != 200:
        abort(result.code, description=result.description)

    data = {'result': 'Successfully Created.'}
    return jsonify(data)


@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product.

    Args:
        product_id (int): id of product to update
        name (str): name of product
        price (int): price of product

    Returns:
        str: json
    """
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

    data = {'result': 'Successfully Updated.'}
    return jsonify(data)


@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product.

    Args:
        product_id (int): id of product to delete

    Returns:
        str: json
    """
    fetch_product_wrapper(product_id)

    result = Product().delete(product_id)
    if result.code != 200:
        abort(result.code, description=result.description)

    data = {'result': 'Successfully Deleted.'}
    return jsonify(data)


def fetch_product_wrapper(product_id):
    """Fetch product.

    Args:
        product_id (int): id of product to fetch

    Returns:
        dict: product info
    """
    result = Product().fetch(product_id)
    if result.code != 200:
        abort(result.code, description=result.description)
    if not result.value:
        abort(404, description='product {0}'.format(product_id))
    return result
