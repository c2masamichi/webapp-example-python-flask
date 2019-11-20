from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            error = User().create(username, password)

        if error is None:
            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('user/create.html')


@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user_client = User()
    if user_client.fetch(user_id) is None:
        abort(404)
    user_client.delete(user_id)
    return redirect(url_for('blog.index'))
