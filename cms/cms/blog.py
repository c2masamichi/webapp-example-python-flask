from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import Entry
from cms.role import Privilege
from cms.role import ROLE_PRIV
from cms.utils import flash_error, flash_success

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Show entries for readers.

    Returns:
        str: template
    """
    result = Entry().fetch_all()
    if not result.succeeded:
        abort(500)
    return render_template('blog/index.html', entries=result.value)


@bp.route('/entry/<int:entry_id>')
def get_entry(entry_id):
    """Show entry.

    Args:
        entry_id (int): id of entry to fetch

    Returns:
        str: template
    """
    entry = fetch_entry_wrapper(entry_id)
    return render_template('blog/detail.html', entry=entry)


@bp.route('/edit/')
@login_required
def edit_top():
    """Show entries for editors.

    Returns:
        str: template
    """
    result = Entry().fetch_all()
    if not result.succeeded:
        abort(500)

    can_update_all_enrty = False
    if ROLE_PRIV[g.user['role']] >= Privilege.EDITOR:
        can_update_all_enrty = True

    return render_template(
        'blog/edit_top.html', entries=result.value,
        can_update_all_enrty=can_update_all_enrty
    )


@bp.route('/edit/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create entry.

    Args:
        title (str): title of entry
        body (str): body of entry

    Returns:
        str: template
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash_error('Title is required.')
        else:
            result = Entry().create(g.user['id'], title, body)
            if result.succeeded:
                flash_success(result.description)
                return redirect(url_for('blog.edit_top'))
            flash_error(result.description)

    return render_template('blog/create.html')


@bp.route('/edit/update/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def update(entry_id):
    """Update entry.

    Args:
        entry_id (int): id of entry to update
        title (str): title of entry
        body (str): body of entry

    Returns:
        str: template
    """
    entry = fetch_entry_wrapper(entry_id)

    if (ROLE_PRIV[g.user['role']] < Privilege.EDITOR and
            entry['author_id'] != g.user['id']):
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash_error('Title is required.')
        else:
            result = Entry().update(entry_id, title, body)
            if result.succeeded:
                flash_success(result.description)
                return redirect(url_for('blog.update', entry_id=entry_id))
            flash_error(result.description)

    return render_template('blog/update.html', entry=entry)


@bp.route('/edit/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id):
    """Delete entry.

    Args:
        entry_id (int): id of entry to delete

    Returns:
        str: template
    """
    entry = fetch_entry_wrapper(entry_id)
    if (ROLE_PRIV[g.user['role']] < Privilege.EDITOR and
            entry['author_id'] != g.user['id']):
        abort(403)

    result = Entry().delete(entry_id)
    if result.succeeded:
        flash_success(result.description)
    else:
        flash_error(result.description)
        render_template('blog/update.html', entry=entry)
    return redirect(url_for('blog.edit_top'))


def fetch_entry_wrapper(entry_id):
    """Fetch entry.

    Args:
        entry_id (int): id of entry to fetch

    Returns:
        dict: entry info
    """
    result = Entry().fetch(entry_id)
    if not result.succeeded:
        abort(500)
    entry = result.value
    if entry is None:
        abort(404)
    return entry
