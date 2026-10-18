
from app import create_app


dev_app = create_app("development")
test_app = create_app("testing")

print("DEV DB:", dev_app.config["DATABASE"])
print("TEST DB:", test_app.config["DATABASE"])
