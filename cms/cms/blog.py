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
from cms.model import Entry

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Entry(db=get_db()).fetch_all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/entry/<int:post_id>')
def get_entry(post_id):
    post = Entry(db=get_db()).fetch(post_id)
    if post is None:
        abort(404)
    return render_template('blog/detail.html', post=post)


@bp.route('/edit/')
@login_required
def list_for_editors():
    posts = Entry(db=get_db()).fetch_all()
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
            Entry(db=get_db()).create(title, body)
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/edit/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Entry(db=get_db()).fetch(post_id)
    if post is None:
        abort(404)

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
    if Entry(db=get_db()).fetch(post_id) is None:
        abort(404)
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'DELETE FROM post WHERE id = %s',
            (post_id,),
        )
    db.commit()
    return redirect(url_for('blog.index'))
