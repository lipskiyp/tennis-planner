# Tennis Planner (In progress)

Django web appllication to manage tennis training sessions with front-end UI, Django REST Framework API and PostgreSQL database management.

### The app implements:

* Custom Docker container environment with version control and two separate services for the Django app and PostgreSQL database.
* Custom Django user model with user email as the primary user identifier.
* Self-contained Django REST Framework API for user, authentication and training session requests.
* Custom query parameters for the API.
* The app supports both, session authentication scheme and token user authentication via the API.
* Custom API permissions with 4 permission groups (user, coach, staff, superuser).
* Auto-genertaed Swagger UI documentation for the REST API.
* (IN PROGRESS) Dynamic front-end implemented in JavaScript using jQuery with AJAX requests to the API.
* Unit tests for the API and back-end of the core app.
* Custom Django commands.

## app/tennis_planner

Django project folder.

## app/core

Django core app with UI.

## /app/api

Django REST Framework API application.

## app/user

Custom user and authentication app.
