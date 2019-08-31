import json

from flask import Blueprint
from flask import current_app
from flask import jsonify
from werkzeug.exceptions import abort

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return 'top'

def load_data(product_id):
    with open(current_app.config['JSON_PATH'], encoding='utf-8') as f:
        data = json.load(f)
        str_id = str(product_id)
        if str_id not in data:
            abort(404)
        return data[str_id]


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    return jsonify(load_data(product_id))