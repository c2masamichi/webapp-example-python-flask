from flask import render_template


def bad_request(e):
    return render_template('error/400.html'), 404


def forbidden(e):
    return render_template('error/403.html'), 404


def not_found(e):
    return render_template('error/404.html'), 404


def internal_server_error(e):
    return render_template('error/500.html'), 404
