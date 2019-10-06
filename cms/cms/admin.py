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
from cms.blog import get_post
from cms.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body) VALUES (:title, :body)',
                {'title': title, 'body': body},
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('admin/create.html')


@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = :title, body = :body WHERE id = :id',
                {'title': title, 'body': body, 'id': post_id},
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('admin/update.html', post=post)


@bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    get_post(post_id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = :id',
        {'id': post_id},
    )
    db.commit()
    return redirect(url_for("blog.index"))


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

    return render_template('admin/register.html')


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
