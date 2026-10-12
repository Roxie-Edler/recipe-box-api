## Acceptance list (public contract)

# Each item: request + expected status + important response details
Total distinct responsibilities in current app.py: 14
Acceptance list (public contract)

Each item defines an externally visible API behavior that must remain unchanged during the refactor.

1. POST /register — Create a new user
Expects: JSON { "username", "email", "password" }
Returns: 201 Created
Body: { "id": number, "username": string, "email": string }
Failures: 400 for missing fields; 409 for duplicate username or email.
2. POST /login — Authenticate a user
Expects: JSON { "username", "password" }
Returns: 200 OK
Body: { "id": number, "username": string, "role": string, "token": string }
Failures: 400 for missing fields; 401 for invalid credentials.
3. GET /recipes/<id> — Read an existing recipe
Auth: None required.
Returns: 200 OK
Body: { "id": number, "title": string, "ingredients": string, "instructions": string, "is_public": boolean }
4. GET /recipes/<id> — Read a nonexistent recipe
Auth: None required.
Returns: 404 Not Found
Body: { "error": "recipe not found" }
5. DELETE /recipes/<id> — Delete an owned recipe
Auth: Valid JWT for the recipe owner or an admin.
Returns: 204 No Content
Body: Empty.
Failures: 401 for authentication failures; 403 for insufficient permissions; 404 if the recipe does not exist.

Total acceptance items so far: 5

Target package layout (planned)
recipe_box/
├── __init__.py
├── config.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── recipes.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   └── recipes.py
└── data/
    ├── __init__.py
    ├── db.py
    ├── recipes.py
    └── users.py

Responsibility mapping

HTTP / API layer

Flask app creation and route registration → recipe_box/__init__.py
User registration and login routes → recipe_box/routes/auth.py
Recipe CRUD routes and HTTP responses → recipe_box/routes/recipes.py
Request validation and API error responses → route modules

Business / service layer

JWT creation and validation → recipe_box/services/auth.py
Password hashing and credential verification → recipe_box/services/auth.py
Recipe ownership and admin checks → recipe_box/services/recipes.py
Recipe-related business rules → recipe_box/services/recipes.py
Recipe response serialization → recipe_box/services/recipes.py

Data / persistence layer

SQLite connection management and foreign-key configuration → recipe_box/data/db.py
Recipe SQL operations → recipe_box/data/recipes.py
User lookup and registration SQL operations → recipe_box/data/users.py
Database integrity and uniqueness conflicts → data modules, with errors translated into HTTP responses by the route or service layer.

Configuration

Environment variables and JWT secret configuration → recipe_box/config.py
Refactoring constraints
Preserve the existing API contract documented in the acceptance list.
Move code into modules without intentionally changing endpoint behavior.
Keep SQL operations out of route handlers.
Keep authentication and ownership rules centralized in services.
Do not move or rewrite implementation code yet; this section describes the intended destination only.