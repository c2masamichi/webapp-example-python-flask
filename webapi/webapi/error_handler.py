from flask import jsonify


def not_found(e):
    return jsonify(error=str(e)), 404
