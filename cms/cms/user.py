from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import admin_required
from cms.auth import login_required
from cms.models import User
from cms.role import make_sorted_roles
from cms.utils import flash_error, flash_success

bp = Blueprint('user', __name__, url_prefix='/admin/auth/user')

roles = make_sorted_roles()


@bp.route('/')
@login_required
@admin_required
def index():
    """Show users.

    Returns:
        str: template
    """
    result = User().fetch_all()
    if not result.succeeded:
        abort(500)
    return render_template('user/index.html', users=result.value)


@bp.route('/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create user.

    Args:
        role (str): user's role
        username (str): user's name
        password (str): user's password

    Returns:
        str: template
    """
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
            flash_error(error)
        else:
            result = User().create(role, username, password)
            if result.succeeded:
                flash_success(result.description)
                return redirect(url_for('user.index'))
            flash_error(result.description)

    return render_template('user/create.html', roles=roles)


@bp.route('<int:user_id>/change/', methods=['GET', 'POST'])
@login_required
@admin_required
def update(user_id):
    """Update user.

    Args:
        user_id (int): id of user to update
        role (str): user's role
        username (str): user's name

    Returns:
        str: template
    """
    user = fetch_user_wrapper(user_id)

    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']

        if not username:
            flash_error('Username is required.')
        else:
            result = User().update(user_id, role, username)
            if result.succeeded:
                flash_success(result.description)
                return redirect(
                    url_for('user.update', user_id=user_id))
            flash_error(result.description)

    return render_template('user/update.html', user=user, roles=roles)


@bp.route('/<int:user_id>/password/', methods=['POST'])
@login_required
@admin_required
def change_password(user_id):
    """Change password.

    Args:
        user_id (int): id of user to change
        new_password (str): password after change

    Returns:
        str: template
    """
    user = fetch_user_wrapper(user_id)

    new_password = request.form['new_password']
    result = User().change_password(
        user_id, new_password, old_required=False)
    if result.succeeded:
        flash_success(result.description)
    else:
        flash_error(result.description)

    return render_template('user/update.html', user=user)


@bp.route('/<int:user_id>/delete/', methods=['POST'])
@login_required
@admin_required
def delete(user_id):
    """Delete user.

    Args:
        user_id (int): id of user to delete

    Returns:
        str: template
    """
    user = fetch_user_wrapper(user_id)
    result = User().delete(user_id)
    if result.succeeded:
        flash_success(result.description)
        return redirect(url_for('user.index'))

    flash_error(result.description)
    return render_template('user/update.html', user=user)


def fetch_user_wrapper(user_id):
    """Fetch user.

    Args:
        user_id (int): id of user to fetch

    Returns:
        dict: user info
    """
    result = User().fetch(user_id)
    if not result.succeeded:
        abort(500)
    user = result.value
    if user is None:
        abort(404)
    return user
