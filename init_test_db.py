
from app import create_app
from app.db import init_db # type: ignore

app = create_app("testing")

with app.app_context():
    init_db(app)

print("Initialized testing database:", app.config["DATABASE"])
