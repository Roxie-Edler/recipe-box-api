
from app.extensions import db  # type: ignore


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    recipes = db.relationship("Recipe", back_populates="owner")

    # Recipes this user has favorited
    favorite_recipes = db.relationship(
        "UserFavorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False, default="")
    is_public = db.Column(db.Integer, nullable=False, default=1)

    # Retained for backward compatibility; not used for new favorites logic
    is_favorite = db.Column(db.Boolean, nullable=True, default=False)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
    )
    owner = db.relationship("User", back_populates="recipes")

    # Users who have favorited this recipe
    favorited_by = db.relationship(
        "UserFavorite",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )


class UserFavorite(db.Model):
    __tablename__ = "user_favorites"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True,
    )

    user = db.relationship("User", back_populates="favorite_recipes")
    recipe = db.relationship("Recipe", back_populates="favorited_by")
