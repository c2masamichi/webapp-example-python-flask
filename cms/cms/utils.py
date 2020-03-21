from flask import flash


def flash_error(message):
    flash(message, category='error')


def flash_success(message):
    flash(message, category='success')
