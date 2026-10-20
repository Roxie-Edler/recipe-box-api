from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()