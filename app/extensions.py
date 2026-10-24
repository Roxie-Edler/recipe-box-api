from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)