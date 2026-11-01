from flask import Blueprint, jsonify, request

from users_service.services.user_service import ( # type: ignore
    InvalidCredentialsError,
    UserAlreadyExistsError,
    login_user,
    register_user,
)

users_bp = Blueprint("users", __name__)


@users_bp.get("/health")
def health():
    return jsonify({"service": "users", "status": "ok"})


@users_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    try:
        result = register_user(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except UserAlreadyExistsError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(result), 201


@users_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    try:
        result = login_user(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except InvalidCredentialsError as exc:
        return jsonify({"error": str(exc)}), 401

    return jsonify(result), 200