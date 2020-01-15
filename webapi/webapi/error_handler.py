from flask import jsonify


def bad_request(e):
    return jsonify(error=str(e)), 400

def not_found(e):
    return jsonify(error=str(e)), 404
