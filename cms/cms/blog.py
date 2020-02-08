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
    entry = fetch_entry_wrapper(entry_id)
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

        if not title:
            flash('Title is required.')
        else:
            result = Entry().create(title, body)
            if result.succeeded:
                return redirect(url_for('blog.edit_top'))
            else:
                flash(result.description)

    return render_template('blog/create.html')


@bp.route('/edit/update/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def update(entry_id):
    entry = fetch_entry_wrapper(entry_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash('Title is required.')
        else:
            result = Entry().update(entry_id, title, body)
            flash(result.description)
            if result.succeeded:
                return redirect(url_for('blog.update', entry_id=entry_id))

    return render_template('blog/update.html', entry=entry)


@bp.route('/edit/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id):
    entry = fetch_entry_wrapper(entry_id)
    result = Entry().delete(entry_id)
    if not result.succeeded:
        flash(result.description)
        render_template('blog/update.html', entry=entry)
    return redirect(url_for('blog.edit_top'))


def fetch_entry_wrapper(entry_id):
    result = Entry().fetch(entry_id)
    if not result.succeeded:
        abort(500)
    entry = result.value
    if entry is None:
        abort(404)
    return entry
