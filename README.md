# FastAPI User Management System

This project is a FastAPI-based application that provides user management functionalities, including the ability to:

- Get all users
- Get a single user by ID
- Add a new user
- Update an existing user by ID
- Delete a user by ID

The application is powered by SQLAlchemy for database interaction, and it includes custom exception handling to ensure robust error reporting. It supports PostgreSQL (or any other database specified in the `.env` file) as the backend database.

## Features

- **Get all users**: Endpoint to retrieve a list of all users from the database.
- **Get a user by ID**: Endpoint to retrieve a specific user by their ID.
- **Add a user**: Endpoint to add a new user to the database.
- **Update a user**: Endpoint to update an existing user's data by their ID.
- **Delete a user**: Endpoint to delete a user by their ID.
- **Database connection management**: Uses SQLAlchemy's session management to handle database interactions.

Set up a virtual environment
It is recommended to use a virtual environment to manage dependencies.

```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install dependencies
Install the required Python packages from requirements.txt.
```
pip install -r requirements.txt
Create a .env file
```

In the root directory of the project, create a .env file to store your environment variables, particularly the database URL.
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Database Setup
Ensure your PostgreSQL (or other database) is running.

Update the DATABASE_URL in your .env file to match your database configuration.

Run the application
To run the FastAPI server, use the following command:
```
uvicorn app.main:app --reload
```
