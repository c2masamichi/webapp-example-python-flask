from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from cms.auth import login_required
from cms.model import User
from cms.user import fetch_user_wrapper

bp = Blueprint('mypage', __name__, url_prefix='/mypage')


@bp.route('/')
@login_required
def index():
    return render_template('mypage/index.html', user=g.user)


@bp.route('/chpasswd', methods=['GET', 'POST'])
@login_required
def change_my_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        result = User().change_password(
            g.user['id'], old_password, new_password
        )
        flash(result.description)

    return render_template('mypage/chpasswd.html', user=g.user)
