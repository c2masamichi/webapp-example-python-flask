import json

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request

from webapi.db import get_db

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return 'top'


def load_all_data():
    db = get_db()
    data = db.execute(
        'SELECT * FROM product'
    ).fetchall()
    result = {
        'result': [
            {
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
            }
            for row in data
        ]
    }
    return result


def load_data(product_id):
    db = get_db()
    row = db.execute(
        'SELECT * FROM product p'
        ' WHERE p.id = :id',
        {'id': product_id},
    ).fetchone()

    if row is None:
        error = {
            'error': 'Not Found.'
        }
        return error, 404

    result =  {
        'result': {
            'id': row['id'],
            'name': row['name'],
            'price': row['price'],
        }
    }
    return result, 200


@bp.route('/products')
def get_products():
    return jsonify(load_all_data())


@bp.route('/products', methods=['POST'])
def post_product():
    if request.headers.get('Content-Type') != 'application/json':
        error = {
            'error': 'Content-Type must be application/json.'
        }
        return jsonify(error), 400

    data = json.loads(request.data)
    name = data.get('name')
    price = data.get('price')
    error_msg = ''
    if name is None or price is None:
        error = {
            'error': 'The key "name" and "price" are required.'
        }
        return jsonify(error), 400

    db = get_db()
    db.execute(
        'INSERT INTO product (name, price) VALUES (:name, :price)',
        {'name': name, 'price': price},
    )
    db.commit()
    result =  {
        'result': 'Successfully Created.'
    }
    return jsonify(result), 201


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    result, code = load_data(product_id)
    return jsonify(result), code
