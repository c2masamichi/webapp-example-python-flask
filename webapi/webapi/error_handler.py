from flask import jsonify


def page_not_found(e):
    return jsonify(error=str(e)), 404
