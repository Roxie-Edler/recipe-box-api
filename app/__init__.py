
from flask import Flask, jsonify
from dotenv import load_dotenv

from config import config_by_name  # type: ignore
from app.extensions import db as sqlalchemy_db # type: ignore
from app.routes.auth import auth_bp  # type: ignore
from app.routes.recipes import recipes_bp  # type: ignore
from app.db import close_db, init_db  # type: ignore


def create_app(config_name="development"):
    load_dotenv()

    app = Flask(__name__)

    # Load the selected configuration.
    chosen_class = config_by_name[config_name]
    app.config.from_object(chosen_class)

    # Initialize SQLAlchemy.
    sqlalchemy_db.init_app(app)

    # Register route blueprints.
    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(recipes_bp, url_prefix="")

    # Clean up the SQLite connection after each request.
    app.teardown_appcontext(close_db)

    # Initialize the existing SQLite database.
    init_db(app)

    @app.get("/")
    def hello():
        return jsonify({
            "message": "Recipe Box API",
            "recipes": "/recipes",
        })

    return app
