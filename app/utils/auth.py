from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"erro": "Token ausente ou inválido"}), 401

        try:
            jwt.decode(token[7:], os.getenv("SECRET_KEY", "dev"), algorithms=["HS256"])
        except Exception as e:
            return jsonify({"erro": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated
