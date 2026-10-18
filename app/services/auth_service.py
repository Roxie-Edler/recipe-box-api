from datetime import datetime, timedelta

import jwt
from flask import current_app, g
import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class InvalidCredentialsError(Exception):
    """Raised when the username or password is incorrect."""

class UserAlreadyExistsError(Exception):
    """Raised when a username or email is already registered."""


def get_db():
    if "db" not in g:
        database = current_app.config["DATABASE"]
        g.db = sqlite3.connect(database)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def register_user(data):
    """Validate and register a user, returning their public details."""
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        raise ValueError(
            "username, email, and password are required"
        )

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
    except sqlite3.IntegrityError as exc:
        db.rollback()
        raise UserAlreadyExistsError(
            "username or email already registered"
        ) from exc

    return {
        "id": cur.lastrowid,
        "username": username,
        "email": email,
    }


def login_user(data):
    """Authenticate a user and return their JWT and public details."""
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise ValueError("Username and password are required")
    
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
        raise InvalidCredentialsError("Invalid credentials")
    
    secret = current_app.config.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not configured")
    
    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256",
    )

    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "token": token,
    }