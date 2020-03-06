from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import User
from cms.model import make_sorted_roles

bp = Blueprint('user', __name__, url_prefix='/user')

roles = make_sorted_roles()


@bp.route('/')
@login_required
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

    return render_template('user/create.html', roles=roles)


@bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
    user = fetch_user_wrapper(user_id)

    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']

        if not username:
            flash('Username is required.')
        else:
            result = User().update(user_id, role, username)
            flash(result.description)
            if result.succeeded:
                return redirect(
                    url_for('user.update', user_id=user_id))

    return render_template('user/update.html', user=user, roles=roles)


@bp.route('/chpasswd/<int:user_id>', methods=['POST'])
@login_required
def change_password(user_id):
    user = fetch_user_wrapper(user_id)

    new_password = request.form['new_password']
    result = User().change_password(
        user_id, new_password, old_required=False)
    flash(result.description)
    return render_template('user/update.html', user=user)


@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    user = fetch_user_wrapper(user_id)
    result = User().delete(user_id)
    if not result.succeeded:
        flash(result.description)
        return render_template('user/update.html', user=user)
    return redirect(url_for('user.index'))


def fetch_user_wrapper(user_id):
    result = User().fetch(user_id)
    if not result.succeeded:
        abort(500)
    user = result.value
    if user is None:
        abort(404)
    return user
