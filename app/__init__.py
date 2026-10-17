from app.routes.auth import auth_bp  # type: ignore
from app.db import get_db, close_db, init_db  # type: ignore
# from app.routes.recipes import recipes_bp  # type: ignore
from app.services.recipe_service import create_recipe_for_user # type: ignore
import os
import sqlite3
from sqlite3 import IntegrityError
from datetime import datetime, timedelta
from functools import wraps

import jwt
from jwt import ExpiredSignatureError
from dotenv import load_dotenv
from flask import Flask, current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from config import config_by_name # type: ignore


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = authenticate_request()
        if result is not None:
            return result

        return fn(*args, **kwargs)

    return wrapper


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
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError as e:
        print("JWT decode error:", repr(e))
        return jsonify({"error": "invalid token"}), 401

    g.current_user = {
        "user_id": int(payload.get("sub")),
        "role": payload.get("role", "user"),
    }

    return None


def recipe_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "ingredients": row["ingredients"],
        "instructions": row["instructions"],
        "is_public": bool(row["is_public"]),
    }


def create_app(config_name="development"):
    app = Flask(__name__)

    chosen_class = config_by_name[config_name]
    app.config.from_object(chosen_class)

    app.register_blueprint(auth_bp, url_prefix="")
    #app.register_blueprint(recipes_bp, url_prefix="")

        # Register database connection cleanup.
    app.teardown_appcontext(close_db)

    # Create database tables if they don't exist.
    init_db(app)



    @app.get("/")
    def hello():
        return jsonify({
            "message": "Recipe Box API",
            "recipes": "/recipes"
        })


    @app.get("/recipes/<int:recipe_id>")
    def get_recipe(recipe_id):
        row = get_db().execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "recipe not found"}), 404

        return jsonify(recipe_to_dict(row))

    
    @app.post("/recipes")
    def create_recipe():
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
                token, secret, algorithms=["HS256"]
            )
        except ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidTokenError as e:
            print("JWT decode error:", repr(e))
            return jsonify({"error": "invalid token"}), 401

        user_id = payload.get("sub")

        data = request.get_json(silent=True)
        if not data or not data.get("title") or not data.get("ingredients"):
            return jsonify({
                "error": "title and ingredients are required"
            }), 400

        try:
            row = create_recipe_for_user(user_id, data)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 409

        return jsonify(recipe_to_dict(row)), 201


    @app.patch("/recipes/<int:recipe_id>")
    @require_auth
    def update_recipe(recipe_id):
        user_id = g.current_user["user_id"]
        role = g.current_user["role"]

        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                "error": "a JSON body is required"
            }), 400

        db = get_db()

        row = db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "recipe not found"}), 404

        if row["owner_id"] != user_id and role != "admin":
            return jsonify({"error": "forbidden"}), 403

        fields = []
        values = []

        for column in ("title", "ingredients", "instructions"):
            if column in data:
                fields.append(f"{column} = ?")
                values.append(data[column])

        if "is_public" in data:
            fields.append("is_public = ?")
            values.append(1 if data["is_public"] else 0)

        if not fields:
            return jsonify({"error": "nothing to update"}), 400

        values.append(recipe_id)

        try:
            db.execute(
                f"UPDATE recipes SET {', '.join(fields)} WHERE id = ?",
                values
            )
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify({
                "error": "a recipe with that title already exists"
            }), 409

        row = db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        return jsonify(recipe_to_dict(row))

    @app.delete("/recipes/<int:recipe_id>")
    @require_auth
    def delete_recipe(recipe_id):
        user_id = g.current_user["user_id"]
        role = g.current_user["role"]

        db = get_db()

        row = db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "recipe not found"}), 404

        if row["owner_id"] != user_id and role != "admin":
            return jsonify({"error": "forbidden"}), 403

        db.execute(
            "DELETE FROM recipes WHERE id = ?",
            (recipe_id,)
        )
        db.commit()

        return "", 204



    return app
