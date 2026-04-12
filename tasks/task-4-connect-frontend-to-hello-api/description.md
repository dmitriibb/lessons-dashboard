# Main Goal
Make the React app call the backend `/hello` API and work both in local development and in Docker Compose.

# Details
The frontend should call the backend `GET /hello` endpoint and display the result in the UI.
This integration must work in two cases:
- when the frontend and backend are both run locally by a developer
- when both apps are run inside Docker Compose

The connection settings should be based on environment variables so the frontend can use different backend URLs in different environments.
The setup should be simple for future API integrations as well.

# Definition of Done
The React app successfully calls the backend `/hello` API and shows the response.
The integration works in local non-Docker development.
The integration also works when frontend and backend are run through Docker Compose.
Environment variables are used to configure the backend base URL.

# Restrictions
Do not hardcode one environment-specific backend URL into the app.
The solution should support both local development and Docker Compose execution.
