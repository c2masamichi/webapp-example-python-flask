from flask import Blueprint
from flask import current_app
from flask import jsonify

from simplewebapi.db import get_db

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
            'error': 'Not Found'
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


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    result, code = load_data(product_id)
    return jsonify(result), code