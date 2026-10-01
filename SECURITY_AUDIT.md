# Security Audit – Recipe API (End-to-End)

Date: 2026-10-01  
Auditor: Roxanne Edler

## 1. Password Storage (Safe Storage)

- **Check:** Inspect `users` table in SQLite.
- **Evidence:**
  ```sql
  PRAGMA table_info(users);
  ```
  Output includes:
  ```text
  3|password_hash|TEXT|1||0
  ```

  ```sql
  SELECT id, email, role, password_hash FROM users LIMIT 3;
  ```
  Example value:
  ```text
  pbkdf2:sha256:1000000$kbmZwkXUA1cIZHZg$f849cf5f1f38fa6bc27e8bf19c14bd1741d69632422a849cd53da1a9c31c8b30
  ```

- **Conclusion:**  
  Passwords are stored as **PBKDF2-SHA256 hashes** in `users.password_hash`.  
  **Result: PASS ✅**

---

## 2. Authentication (Identity Enforcement)

### Anonymous DELETE

- **Request:**
  ```bash
  curl -i -X DELETE http://localhost:5000/recipes/1
  ```
- **Response:**
  ```text
  HTTP/1.1 401 UNAUTHORIZED
  {
    "error": "Missing or invalid Authorization header"
  }
  ```

- **Conclusion:**  
  Anonymous users cannot delete recipes; auth is enforced on DELETE.  
  **Result: PASS ✅**

---

## 3. Authorization (Access Control)

### 3.1 Owner/Admin deletes own recipe

- **Request (owneruser, role=admin):**
  ```bash
  curl -i -X DELETE http://localhost:5000/recipes/8 \
    -H "Authorization: Bearer <OWNERUSER_ADMIN_TOKEN>"
  ```
- **Response:**
  ```text
  HTTP/1.1 204 NO CONTENT
  ```

- **Conclusion:**  
  Owner/admin can delete their own recipe successfully.  
  **Result: PASS ✅**

---

### 3.2 Non-owner tries to delete another user’s recipe

- **Request (otheruser, role=user):**
  ```bash
  curl -i -X DELETE http://localhost:5000/recipes/8 \
    -H "Authorization: Bearer <OTHERUSER_TOKEN>"
  ```
- **Response:**
  ```text
  HTTP/1.1 403 FORBIDDEN
  {
    "error": "forbidden"
  }
  ```

- **Conclusion:**  
  Authenticated non-owner is blocked from deleting another user’s recipe.  
  **Result: PASS ✅**

---

## 4. Overall Conclusion

- **Password storage:** Hashed with PBKDF2-SHA256 – no plaintext credentials.  
- **Authentication:** Protected delete route returns 401 for anonymous requests.  
- **Authorization:** Ownership and roles enforced:
  - Owner/admin can delete own resources.
  - Non-owner users receive 403 when targeting others’ resources.

All tested delete-related paths behave as expected under the current design.