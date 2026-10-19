from app import create_app
from app.extensions import db  # type: ignore

app = create_app("testing")

with app.app_context():
    db.create_all()

print("Initialized testing database:", app.config["DATABASE"])