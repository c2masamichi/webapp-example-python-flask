from flask import render_template


def not_found(e):
    return render_template('error/404.html'), 404
