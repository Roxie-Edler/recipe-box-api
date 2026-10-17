from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError
from datetime import datetime, timedelta
import sqlite3
import jwt


auth_bp = Blueprint("auth", __name__)

def get_db():
    if "db" not in g:
        database = current_app.config["DATABASE"]
        g.db = sqlite3.connect(database)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "error": "username, email, and password are required"
        }), 400

    password_hash = generate_password_hash(
        password, method="pbkdf2:sha256"
    )

    db = get_db()

    try:
        cur = db.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash),
        )
        db.commit()
    except IntegrityError:
        return jsonify({
            "error": "username or email already registered"
        }), 409

    return jsonify({
        "id": cur.lastrowid,
        "username": username,
        "email": email,
    }), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    db = get_db()

    user = db.execute(
        """
        SELECT id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    if user is None or not check_password_hash(
        user["password_hash"], password
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    secret = current_app.config.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not configured")

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256",
    )

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "token": token,
    }), 200