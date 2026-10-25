
def recipe_to_dict(recipe):
    """Convert a SQLAlchemy Recipe instance to a dictionary."""
    return {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "is_public": bool(recipe.is_public),
    }
