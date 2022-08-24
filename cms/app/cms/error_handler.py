from flask import render_template


def forbidden(e):
    return render_template('error/403.html'), 403


def not_found(e):
    return render_template('error/404.html'), 404
