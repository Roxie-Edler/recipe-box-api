
def recipe_to_dict(recipe):
    """Convert either a SQLAlchemy Recipe or sqlite3.Row to a dictionary."""

    def get_value(key):
        # sqlite3.Row supports dictionary-style access.
        try:
            return recipe[key]
        except (TypeError, KeyError, IndexError):
            # SQLAlchemy model instances use attribute access.
            return getattr(recipe, key)

    return {
        "id": get_value("id"),
        "title": get_value("title"),
        "ingredients": get_value("ingredients"),
        "instructions": get_value("instructions"),
        "is_public": bool(get_value("is_public")),
    }
