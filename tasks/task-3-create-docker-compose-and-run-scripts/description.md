# Main Goal
Create Docker Compose setup for the backend, frontend, and MariaDB, and add scripts for Ubuntu and Windows to build and run it.

# Details
Add Docker Compose configuration that runs:
- the Go backend app
- the React frontend app
- the MariaDB database

Also add scripts for both Ubuntu and Windows that:
- build the Docker images if needed
- start the Docker Compose setup

The scripts should be easy to run by a developer on the corresponding operating system.
This task is only about local and simple deployment setup, not production hardening yet.

# Definition of Done
There is a Docker Compose configuration in the repository for backend, frontend, and MariaDB.
There is a script for Ubuntu and a script for Windows to build and run the Compose setup.
A developer can use the provided scripts to start the full local stack.

# Restrictions
Use MariaDB as the database service.
Keep the setup simple and understandable.
Do not over-engineer production infrastructure details in this task.
