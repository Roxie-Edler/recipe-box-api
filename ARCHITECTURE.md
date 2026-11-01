Architecture: Microservice Data Ownership
Users Service

Owns: User accounts and authentication.

Database tables:

users

Data:

User ID
Username
Email
Password hash
Role

Responsibilities:

User registration
User login
Password hashing and verification
JWT generation
User account management
Role management

The Users service is the only service permitted to read or modify user account records.

Recipes Service

Owns: Recipes and recipe-related interactions.

Database tables:

recipes
user_favorites

Data:

Recipe ID
Title
Ingredients
Instructions
Public/private visibility
Owner ID (reference to Users service)
User ID and recipe ID in favorites

Responsibilities:

Creating, reading, updating, and deleting recipes
Managing recipe visibility
Managing recipe ownership references
Managing recipe favorites
Enforcing recipe ownership and authorization

The Recipes service must not directly access the Users database.

User IDs are stored as references only.

API Gateway

Owns: No persistent data and no database tables.

Responsibilities:

Receiving client requests
Forwarding authentication requests to Users
Forwarding recipe requests to Recipes
Combining service responses when necessary
Returning responses to clients

The Gateway does not directly access either service database.

Communication Rules
Each service owns its own database tables.
Services communicate through APIs, never by querying another service's tables.
Users is responsible for authentication and issuing JWTs.
Recipes validates trusted identity information before authorizing recipe operations.
The Gateway owns no business data.
Cross-service references use identifiers rather than database relationships.
Architecture Goal

Create independently maintainable Users and Recipes services, coordinated through a stateless API Gateway.