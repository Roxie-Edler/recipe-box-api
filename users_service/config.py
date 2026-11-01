import os
from dotenv import load_dotenv

load_dotenv()

class UsersConfig:
    SECRET_KEY = os.getenv("USERS_SECRET_KEY", "dev-users-secret")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "USERS_DATABASE_URL",
        "sqlite:///users_service.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "dev-users-jwt-secret"
)