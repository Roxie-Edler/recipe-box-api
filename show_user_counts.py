
import sqlite3

from app import create_app


dev_app = create_app("development")
test_app = create_app("testing")


def count_users(database_path):
    with sqlite3.connect(database_path) as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]


print("DEV users:", count_users(dev_app.config["DATABASE"]))
print("TEST users:", count_users(test_app.config["DATABASE"]))
