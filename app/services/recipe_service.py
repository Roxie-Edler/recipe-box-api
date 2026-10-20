from sqlalchemy.exc import IntegrityError
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
    recipe = Recipe(
        title=data["title"],
        ingredients=data["ingredients"],
        instructions=data.get("instructions", ""),
        is_public=1 if data.get("is_public", True) else 0,
        owner_id=user_id,
    )

    try:
        db.session.add(recipe)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        error_message = str(exc.orig).lower()
        
        if "foreign key" in error_message:
            raise ValueError("invalid owner") from exc

        raise ValueError(
            "a recipe with that title already exists"
        ) from exc

    return recipe

def update_recipe_for_user(recipe_id, user_id, role, data):
    recipe = db.session.get(Recipe, recipe_id)
    if recipe is None:
        return None
    
    if (recipe.owner is None or recipe.owner.id != user_id) and role != "admin":
        raise PermissionError("forbidden")

    for field in ("title", "ingredients", "instructions", "is_public"):
        if field in data:
            setattr(recipe, field, int(bool(data[field])) if field == "is_public" else data[field])
    
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError("a recipe with that title already exists") from exc

    return recipe

def delete_recipe_for_user(recipe_id, user_id, role):
    recipe = db.session.get(Recipe, recipe_id)

    if recipe is None:
        return None

    if (recipe.owner is None or recipe.owner.id != user_id) and role != "admin":
        raise PermissionError("forbidden")

    db.session.delete(recipe)
    db.session.commit()

    return True

def get_recipe_count():
    """Return the total number of recipes."""
    count = db.session.query(db.func.count(Recipe.id)).scalar()
    return {"count": count}
