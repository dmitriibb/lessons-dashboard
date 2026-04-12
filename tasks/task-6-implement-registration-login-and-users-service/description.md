# Main Goal
Implement backend registration, login, and users service with Basic Auth protection for non-registration APIs.

# Details
Implement a simple users service in the Go backend.
Users register using email and password.
Passwords must not be stored in plain text.
Store passwords in hashed form.

Use the following data model requirements:
- users table:
  - `user_id`: long
  - `email`: varchar
  - `first_name`: nullable
  - `last_name`: nullable
- password table:
  - `user_id`
  - `pwd`

The password hash must be stored in the separate password table.

Implement registration and login backend APIs.
For now, all backend APIs except registration should be protected with Basic Auth.

This task should include the necessary backend logic, persistence, validation, and authentication handling needed for this first version.

# Definition of Done
There is a backend registration API that creates a user with email and hashed password.
There is a backend login API.
User data is stored in the users table with the required fields.
Password hashes are stored in a separate password table linked by `user_id`.
All APIs except registration are protected by Basic Auth.

# Restrictions
Do not store raw passwords.
Use secure password hashing.
Keep the implementation simple but reliable.
The required table split between user data and password hash data must be respected.
