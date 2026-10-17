
import sqlite3

from app.db import get_db # type: ignore


def create_recipe_for_user(user_id, data):
    """Create a recipe for a user and return the inserted database row."""
    db = get_db()

    try:
        cursor = db.execute(
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
        db.commit()
    except sqlite3.IntegrityError as exc:
        raise ValueError(
            "a recipe with that title already exists"
        ) from exc

    row = db.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()

    return row
