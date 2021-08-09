import functools

from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.exceptions import abort

from cms.models import User
from cms.role import Privilege
from cms.role import ROLE_PRIV
from cms.user_wrappers import auth_user
from cms.user_wrappers import change_password
from cms.utils import flash_error, flash_success

bp = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if ROLE_PRIV[g.user.role] < Privilege.ADMINISTRATOR:
            abort(403)

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.query.get(user_id)
        if user is None:
            abort(500)
        g.user = user


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Log in by username and password.

    Args:
        name (str): user's name
        password (str): user's password

    Returns:
        str: template
    """
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        user = auth_user(name, password)
        if user is not None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.admin_top'))

        flash_error('Incorrect username or password.')

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Log out of the site.

    Returns:
        str: template
    """
    session.clear()
    flash_success('Logged out.')
    return redirect(url_for('index'))


@bp.route('/admin/')
@login_required
def admin_top():
    """Site administration top page.

    Returns:
        str: template
    """
    return render_template('auth/admin_top.html')


@bp.route('/admin/password_change/', methods=['GET', 'POST'])
@login_required
def change_my_password():
    """Change own password.

    Args:
        old_password (str): current password
        new_password (str): password after change

    Returns:
        str: template
    """
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        succeeded, message = change_password(
            g.user.id, new_password, old_password)
        if succeeded:
            flash_success(message)
        else:
            flash_error(message)

    return render_template('auth/chpasswd.html', user=g.user)
