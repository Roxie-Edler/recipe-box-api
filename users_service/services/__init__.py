from datetime import datetime, timedelta

import jwt
from flask import current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from users_service.extensions import db # type: ignore
from users_service.models import User # type: ignore


class InvalidCredentialsError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


def register_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        raise ValueError(
            "username, email, and password are required"
        )

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(
            password,
            method="pbkdf2:sha256",
        ),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise UserAlreadyExistsError(
            "username or email already registered"
        ) from exc

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise ValueError(
            "Username and password are required"
        )

    user = User.query.filter_by(
        username=username
    ).first()

    if user is None or not check_password_hash(
        user.password_hash,
        password,
    ):
        raise InvalidCredentialsError(
            "Invalid credentials"
        )

    secret = current_app.config.get("JWT_SECRET")

    if not secret:
        raise RuntimeError(
            "JWT_SECRET is not configured"
        )

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256",
    )

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "token": token,
    }