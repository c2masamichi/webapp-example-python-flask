import json

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
    result = [
        {
            'id': row['id'],
            'name': row['name'],
            'price': row['price'],
        }
        for row in data
    ]
    return {
        'result': result
    }


def load_data(product_id):
    with open(current_app.config['JSON_PATH'], encoding='utf-8') as f:
        data = json.load(f)
        str_id = str(product_id)
        if str_id in data:
            resp = {
                'result': data[str_id]
            }
            return resp, 200
        else:
            error = {
                'error': 'Not Found'
            }
            return error, 404


@bp.route('/products')
def get_products():
    return jsonify(load_all_data())


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    result, code = load_data(product_id)
    return jsonify(result), code