
from functools import wraps

import jwt
from jwt import ExpiredSignatureError
from flask import current_app, g, jsonify, request


def authenticate_request():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return jsonify({
            "error": "Missing or invalid Authorization header"
        }), 401

    token = auth_header.split(" ", 1)[1].strip()

    secret = current_app.config.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not configured")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "invalid token"}), 401

    g.current_user = {
        "user_id": user_id,
        "role": payload.get("role", "user"),
    }

    return None


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = authenticate_request()

        if result is not None:
            return result

        return fn(*args, **kwargs)

    return wrapper
