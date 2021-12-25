from flask import jsonify


def bad_request(e):
    return jsonify(error=str(e)), 400

def not_found(e):
    return jsonify(error=str(e)), 404

def internal_server_error(e):
    return jsonify(error=str(e)), 500
