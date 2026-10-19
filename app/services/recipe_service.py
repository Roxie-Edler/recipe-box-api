
import sqlite3

from app.db import get_db # type: ignore
from app.extensions import db # type: ignore
from app.models import Recipe # type: ignore


def list_recipes():
    """Return all recipes ordered by ID."""
    return Recipe.query.order_by(Recipe.id).all()


def get_recipe_by_id(recipe_id):
    """Return a recipe by ID, or None if it doesn't exist."""
    return db.session.get(Recipe, recipe_id)


def create_recipe_for_user(user_id, data):
    """Create a recipe for a user and return the inserted database row."""
    database = get_db()

    try:
        cursor = database.execute(
            """
            INSERT INTO recipes
                (title, ingredients, instructions, is_public, owner_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["title"],
                data["ingredients"],
                data.get("instructions", ""),
                1 if data.get("is_public", True) else 0,
                user_id,
            ),
        )
        database.commit()
    except sqlite3.IntegrityError as exc:
        raise ValueError(
            "a recipe with that title already exists"
        ) from exc

    return database.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()


def get_recipe_count():
    """Return the total number of recipes."""
    database = get_db()
    row = database.execute(
        "SELECT COUNT(*) AS count FROM recipes"
    ).fetchone()

    return {"count": row["count"]}

