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
    with db.cursor() as cursor:
        cursor.execute(
            'SELECT title, body, created FROM post'
            ' ORDER BY created DESC'
        )
        posts = cursor.fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/entry/<int:post_id>')
def get_entry(post_id):
    post = get_post(post_id)
    return render_template('blog/detail.html', post=post)


@bp.route('/edit/')
@login_required
def list_for_editors():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'SELECT title, body, created FROM post'
            ' ORDER BY created DESC'
        )
        posts = cursor.fetchall()
    return render_template('blog/list.html', posts=posts)


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
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO post (title, body) VALUES (%s, %s)',
                    (title, body),
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
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE post SET title = %s, body = %s WHERE id = %s',
                    (title, body, post_id),
                )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/edit/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    get_post(post_id)
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'DELETE FROM post WHERE id = %s',
            (post_id,),
        )
    db.commit()
    return redirect(url_for('blog.index'))


def get_post(post_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'SELECT id, title, body, created FROM post WHERE id = %s',
            (post_id,),
        )
        post = cursor.fetchone()

    if post is None:
        abort(404)

    return post
