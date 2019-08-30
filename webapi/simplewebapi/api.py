from flask import Blueprint

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'top'

@bp.route('/product/<int:product_id>')
def get_product(product_id):
    return 'get {0}'.format(product_id)
