from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    result = User().fetch_all()
    if not result.succeeded:
        abort(500)
    return render_template('user/index.html', users=result.value)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        error = ''
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error:
            flash(error)
        else:
            result = User().create(role, username, password)
            if result.succeeded:
                return redirect(url_for('user.index'))
            else:
                flash(result.description)

    return render_template('user/create.html')


@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    user_client = User()
    if user_client.fetch(user_id) is None:
        abort(404)
    result = user_client.delete(user_id)
    if not result.succeeded:
        flash(result.description)
    return redirect(url_for('user.index'))
