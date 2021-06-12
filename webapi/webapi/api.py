from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from webapi.database import db
from webapi.models import Product

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/products')
def get_products():
    """Fetch products.

    Returns:
        str: json
    """
    result = Product.query.all()
    data = {
        'result': [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
            }
            for product in result
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
    product = Product.query.get_or_404(product_id)

    data = {
        'result': {
            'id': product.id,
            'name': product.name,
            'price': product.price,
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

    try:
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
    except AssertionError:
        abort(400, description='Bad data.')

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

    product = Product.query.get_or_404(product_id)

    try:
        product.name = name
        product.price = price
        db.session.commit()
    except AssertionError:
        abort(400, description='Bad data.')

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
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()
    data = {'result': 'Successfully Deleted.'}
    return jsonify(data)
