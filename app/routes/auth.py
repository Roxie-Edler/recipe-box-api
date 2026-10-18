
from flask import Blueprint, request, jsonify

from app.services.auth_service import (
    register_user,
    login_user,
    UserAlreadyExistsError,
    InvalidCredentialsError,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    try:
        result = register_user(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except UserAlreadyExistsError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(result), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    try:
        result = login_user(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except InvalidCredentialsError as exc:
        return jsonify({"error": str(exc)}), 401

    return jsonify(result), 200