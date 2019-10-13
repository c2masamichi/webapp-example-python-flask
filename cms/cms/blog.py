from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT title, body, created FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/entry/<int:post_id>')
def get_entry(post_id):
    post = get_post(post_id)
    return render_template('blog/detail.html', post=post)


@bp.route('/edit/create', methods=['GET', 'POST'])
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

    return render_template('blog/create.html')


@bp.route('/edit/update/<int:post_id>', methods=['GET', 'POST'])
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

    return render_template('blog/update.html', post=post)


@bp.route('/edit/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    get_post(post_id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = :id',
        {'id': post_id},
    )
    db.commit()
    return redirect(url_for('blog.index'))


def get_post(post_id):
    db = get_db()
    post = db.execute(
        'SELECT id, title, body, created FROM post'
        ' WHERE id = :id',
        {'id': post_id},
    ).fetchone()

    if post is None:
        abort(404)

    return post
