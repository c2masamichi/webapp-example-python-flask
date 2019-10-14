from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from cms.auth import login_required
from cms.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif (
            db.execute(
                'SELECT id FROM user WHERE username = ?',
                (username,)
            ).fetchone()
            is not None
        ):
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('user/register.html')


@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    get_user(user_id)
    db = get_db()
    db.execute(
        'DELETE FROM user WHERE id = :id',
        {'id': user_id},
    )
    db.commit()
    return redirect(url_for('blog.index'))


def get_user(user_id):
    db = get_db()
    user = db.execute(
        'SELECT id, username FROM user'
        ' WHERE id = :id',
        {'id': user_id},
    ).fetchone()

    if user is None:
        abort(404)

    return user
