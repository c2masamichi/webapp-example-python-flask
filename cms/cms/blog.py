from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import Entry

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    result = Entry().fetch_all()
    if not result.succeeded:
        abort(500)
    return render_template('blog/index.html', entries=result.value)


@bp.route('/entry/<int:entry_id>')
def get_entry(entry_id):
    entry = Entry().fetch(entry_id)
    if entry is None:
        abort(404)
    return render_template('blog/detail.html', entry=entry)


@bp.route('/edit/')
@login_required
def edit_top():
    result = Entry().fetch_all()
    if not result.succeeded:
        abort(500)
    return render_template('blog/edit_top.html', entries=result.value)


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
            Entry().create(title, body)
            return redirect(url_for('blog.edit_top'))

    return render_template('blog/create.html')


@bp.route('/edit/update/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def update(entry_id):
    entry_client = Entry()
    entry = entry_client.fetch(entry_id)
    if entry is None:
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
            entry_client.update(entry_id, title, body)
            flash('Update succeeded!')
            return redirect(url_for('blog.update', entry_id=entry_id))

    return render_template('blog/update.html', entry=entry)


@bp.route('/edit/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id):
    entry_client = Entry()
    if entry_client.fetch(entry_id) is None:
        abort(404)
    entry_client.delete(entry_id)
    return redirect(url_for('blog.edit_top'))
