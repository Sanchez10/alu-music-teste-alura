from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_app.config.get("TESTING"):
            return f(*args, **kwargs)

        token = request.headers.get('Authorization')

        if not token or not token.startswith("Bearer "):
            return jsonify({"erro": "Token ausente ou inválido"}), 401

        return f(*args, **kwargs)
    return decorated
