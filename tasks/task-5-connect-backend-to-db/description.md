# Main Goal
Connect the backend to the database using connection pooling and an ORM.

# Details
Update the Go backend so it connects to the MariaDB database.
The database access layer should use connection pooling.
Use a suitable Go ORM if it improves the implementation quality and developer productivity.
If using a framework in Go helps with this task, that is allowed.

This task is about establishing the database integration foundation for future backend features.
The implementation should prepare the backend for working with real application data.

# Definition of Done
The backend successfully connects to MariaDB.
Database access uses a connection pool.
An ORM or similarly structured database layer is set up and integrated into the backend.
The setup is ready for future user-related and application-related persistence work.

# Restrictions
Use MariaDB for the database.
Favor a well-supported and maintainable Go database solution.
Avoid unnecessary complexity, but the user is fine with using frameworks if there is a strong reason.
