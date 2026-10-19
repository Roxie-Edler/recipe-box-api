import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    DATABASE = os.getenv("DATABASE_PATH")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    DEBUG = os.getenv("DEBUG", "False") == "True"

    if JWT_SECRET is None:
        raise RuntimeError("JWT_SECRET environment variable is required")
    if DATABASE is None:
        raise RuntimeError("DATABASE_PATH environment variable is required")


class DevelopmentConfig(Config):
    pass
    


class TestingConfig(Config):
    TESTING = True
    DATABASE = os.getenv("TEST_DATABASE_PATH")

    if not DATABASE:
        raise RuntimeError("TEST_DATABASE_PATH is not configured")


class ProductionConfig(Config):
    pass


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
