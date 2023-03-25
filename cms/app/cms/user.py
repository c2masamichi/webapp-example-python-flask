from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.security import generate_password_hash

from cms.auth import admin_required
from cms.auth import login_required
from cms.database import db
from cms.models import User
from cms.role import make_sorted_roles
from cms.user_wrappers import change_password
from cms.user_wrappers import validate_password
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
    users = db.session.query(User).\
        order_by(User.name).\
        all()
    return render_template('user/index.html', users=users)


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
        elif not validate_password(password):
            error = 'Bad data.'
        elif User.query.filter_by(name=username).first() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error:
            flash_error(error)
        else:
            try:
                user = User(
                    role=role, name=username,
                    password=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            except AssertionError:
                flash_error('Bad data.')
            else:
                flash_success('Creation succeeded.')
                return redirect(url_for('user.index'))

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
    user = db.get_or_404(User, user_id)

    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']

        error = ''
        if not username:
            error = 'Username is required.'
        elif User.query.filter_by(name=username).first() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error:
            flash_error(error)
        else:
            try:
                user.role = role
                user.name = username
                db.session.commit()
            except AssertionError:
                flash_error('Bad data.')
            else:
                flash_success('Update succeeded.')
                return redirect(
                    url_for('user.update', user_id=user_id))

    return render_template('user/update.html', user=user, roles=roles)


@bp.route('/<int:user_id>/password/', methods=['POST'])
@login_required
@admin_required
def change_user_password(user_id):
    """Change password.

    Args:
        user_id (int): id of user to change
        new_password (str): password after change

    Returns:
        str: template
    """
    user = db.get_or_404(User, user_id)

    new_password = request.form['new_password']
    succeeded, message = change_password(
        user_id, new_password, old_required=False)
    if succeeded:
        flash_success(message)
    else:
        flash_error(message)

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
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    flash_success('Deletion succeeded.')
    return redirect(url_for('user.index'))
