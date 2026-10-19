from app.models import Recipe # type: ignore
from app.extensions import db # type: ignore
from app.services.recipe_service import list_recipes as list_recipes_orm, get_recipe_by_id # type: ignore
import sqlite3

import jwt
from jwt import ExpiredSignatureError
from flask import Blueprint, request, jsonify, current_app, g

from app.db import get_db # type: ignore
from app.auth_utils import require_auth # type: ignore
from app.services.recipe_service import ( # type: ignore
    create_recipe_for_user,
    get_recipe_count,
    list_recipes,
    get_recipe_by_id,
)
from app.utils import recipe_to_dict # type: ignore


recipes_bp = Blueprint("recipes", __name__)



@recipes_bp.get("/recipes")
def list_recipes():
    recipes = list_recipes_orm()
    return jsonify([{
        "id": r.id,
        "title": r.title,
        "ingredients": r.ingredients,
        "instructions": r.instructions,
        "is_public": r.is_public,
        "owner_id": r.owner_id,
    } for r in recipes])


@recipes_bp.get("/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)

    if recipe is None:
        return jsonify({"error": "recipe not found"}), 404

    return jsonify({
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "is_public": recipe.is_public,
        "owner_id": recipe.owner_id,
    })


@recipes_bp.post("/recipes")
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
            token,
            secret,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401

    user_id = payload.get("sub")

    data = request.get_json(silent=True)

    if (
        not data
        or not data.get("title")
        or not data.get("ingredients")
    ):
        return jsonify({
            "error": "title and ingredients are required"
        }), 400

    try:
        row = create_recipe_for_user(user_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(recipe_to_dict(row)), 201


@recipes_bp.patch("/recipes/<int:recipe_id>")
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
        (recipe_id,),
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
            values,
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "error": "a recipe with that title already exists"
        }), 409

    row = db.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()

    return jsonify(recipe_to_dict(row)), 200


@recipes_bp.delete("/recipes/<int:recipe_id>")
@require_auth
def delete_recipe(recipe_id):
    user_id = g.current_user["user_id"]
    role = g.current_user["role"]

    db = get_db()

    row = db.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()

    if row is None:
        return jsonify({"error": "recipe not found"}), 404

    if row["owner_id"] != user_id and role != "admin":
        return jsonify({"error": "forbidden"}), 403

    db.execute(
        "DELETE FROM recipes WHERE id = ?",
        (recipe_id,),
    )
    db.commit()

    return "", 204


@recipes_bp.get("/recipes/count")
def recipe_count():
    result = get_recipe_count()
    return jsonify(result), 200
