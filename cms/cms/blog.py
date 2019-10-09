from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

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
