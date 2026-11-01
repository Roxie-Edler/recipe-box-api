from flask import Flask
from flask_migrate import Migrate

from users_service.config import UsersConfig # type: ignore
from users_service.extensions import db, migrate # type: ignore
from users_service.routes import users_bp # type: ignore
from users_service import models # type: ignore


migrate = Migrate()


def create_app(config_class=UsersConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)

    return app