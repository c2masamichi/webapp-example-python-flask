from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.blog import get_post
from cms.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/create', methods=['GET', 'POST'])
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
def delete(post_id):
    get_post(post_id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = :id',
        {'id': post_id},
    )
    db.commit()
    return redirect(url_for("blog.index"))
