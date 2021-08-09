from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from sqlalchemy import desc
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.database import db
from cms.models import Entry
from cms.models import User
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
    entries = db.session.query(Entry).\
        order_by(desc(Entry.created)).\
        all()
    return render_template('blog/index.html', entries=entries)


@bp.route('/entry/<int:entry_id>')
def get_entry(entry_id):
    """Show entry.

    Args:
        entry_id (int): id of entry to fetch

    Returns:
        str: template
    """
    entry = Entry.query.get_or_404(entry_id)
    return render_template('blog/detail.html', entry=entry)


@bp.route('/admin/blog/entry/')
@login_required
def edit_top():
    """Show entries for editors.

    Returns:
        str: template
    """
    entries = db.session.query(
            Entry.id, Entry.title, Entry.created, Entry.author_id, User.name).\
        outerjoin(User, Entry.author_id == User.id).\
        order_by(desc(Entry.created)).\
        all()

    can_update_all_enrty = False
    if ROLE_PRIV[g.user.role] >= Privilege.EDITOR:
        can_update_all_enrty = True

    return render_template(
        'blog/edit_top.html', entries=entries,
        can_update_all_enrty=can_update_all_enrty
    )


@bp.route('/admin/blog/entry/add/', methods=['GET', 'POST'])
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
            try:
                entry = Entry(title=title, body=body, author_id=g.user.id)
                db.session.add(entry)
                db.session.commit()
            except AssertionError:
                flash_error('Bad data.')
            else:
                flash_success('Creation succeeded.')
                return redirect(url_for('blog.edit_top'))

    return render_template('blog/create.html')


@bp.route('/admin/blog/entry/<int:entry_id>/change', methods=['GET', 'POST'])
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
    entry = Entry.query.get_or_404(entry_id)

    if (ROLE_PRIV[g.user.role] < Privilege.EDITOR and
            entry.author_id != g.user.id):
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash_error('Title is required.')
        else:
            try:
                entry.title = title
                entry.body = body
                db.session.commit()
            except AssertionError:
                flash_error('Bad data.')
            else:
                flash_success('Update succeeded.')
                return redirect(url_for('blog.update', entry_id=entry_id))

    return render_template('blog/update.html', entry=entry)


@bp.route('/admin/blog/entry/<int:entry_id>//delete', methods=['POST'])
@login_required
def delete(entry_id):
    """Delete entry.

    Args:
        entry_id (int): id of entry to delete

    Returns:
        str: template
    """
    entry = Entry.query.get_or_404(entry_id)
    if (ROLE_PRIV[g.user.role] < Privilege.EDITOR and
            entry.author_id != g.user.id):
        abort(403)

    db.session.delete(entry)
    db.session.commit()

    flash_success('Deletion succeeded.')
    return redirect(url_for('blog.edit_top'))
