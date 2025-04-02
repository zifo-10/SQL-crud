from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.database import Base, SessionLocal, engine
from app.exception.custom_exception import CustomException, CustomHTTPException
from app.models import User
from app.schema.user_schema import CreateUserSchema, GetUserSchema, UpdateUserSchema

# Create the FastAPI app
app = FastAPI()


# Dependency to get DB session
def get_db():
    """
    Dependency to get a database session.
    Ensures that the session is properly closed after use.

    Raises:
        CustomException: If there is an error connecting to the database.
    """
    try:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database.",
            exception_type="DatabaseConnectionError",
            additional_info={"error": str(e)}
        )


# Create the table if it does not exist
@app.on_event("startup")
def create_tables():
    """
    Event handler to create all tables at the startup of the app.
    It ensures that all tables defined by the Base metadata are created in the database.

    Raises:
        CustomException: If there is an error while creating database tables.
    """
    try:
        # Create all tables defined by the Base metadata
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating database tables.",
            exception_type="TableCreationError",
            additional_info={"error": str(e)}
        )


# Route to get all users from the database
@app.get("/users", response_model=list[GetUserSchema])
def get_users(db: Session = Depends(get_db)):
    """
    Route to retrieve all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[GetUserSchema]: A list of all users in the database.

    Raises:
        CustomHTTPException: If no users are found or if there is an error during retrieval.
    """
    try:
        users = db.query(User).all()
        if not users:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found in the database.",
                exception_type="NotFoundError",
                additional_info={}
            )
        return users
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users from the database.",
            exception_type="DatabaseError",
            additional_info={"error": str(e)}
        )


# Route to get a single user by ID from the database
@app.get("/users/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Route to retrieve a single user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        GetUserSchema: The user data corresponding to the provided user ID.

    Raises:
        CustomHTTPException: If the user is not found or if there is an error during retrieval.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the provided ID does not exist.",
                exception_type="NotFoundError",
                additional_info={"user_id": user_id}
            )
        return user
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data from the database.",
            exception_type="DatabaseError",
            additional_info={"error": str(e)}
        )


# Route to add a new user to the database
@app.post("/users", response_model=GetUserSchema)
def add_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    """
    Route to add a new user to the database.

    Args:
        user (CreateUserSchema): The user data to create a new user.
        db (Session): The database session.

    Returns:
        GetUserSchema: The created user data.

    Raises:
        CustomHTTPException: If the email is already registered or if there is an error during the creation process.
    """
    try:
        # Check if the email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered.",
                exception_type="ConflictError",
                additional_info={"email": user.email}
            )

        # Create the new user
        new_user = User(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while adding the user to the database.",
            exception_type="DatabaseError",
            additional_info={"error": str(e)}
        )


# Route to update an existing user by ID
@app.put("/users/{user_id}", response_model=GetUserSchema)
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db)):
    """
    Route to update an existing user's data by their ID.

    Args:
        user_id (int): The ID of the user to update.
        user (UpdateUserSchema): The new data to update the user with.
        db (Session): The database session.

    Returns:
        GetUserSchema: The updated user data.

    Raises:
        CustomHTTPException: If the user does not exist or if there is an error during the update process.
    """
    try:
        # Find the existing user
        existing_user = db.query(User).filter(User.id == user_id).first()
        if existing_user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the provided ID does not exist.",
                exception_type="NotFoundError",
                additional_info={"user_id": user_id}
            )

        # Update the user's fields
        existing_user.name = user.name
        existing_user.email = user.email

        db.commit()
        db.refresh(existing_user)
        return existing_user
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while updating the user data in the database.",
            exception_type="DatabaseError",
            additional_info={"error": str(e)}
        )


# Route to delete a user by ID
@app.delete("/users/{user_id}", response_model=GetUserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Route to delete a user from the database by their ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): The database session.

    Returns:
        GetUserSchema: The deleted user data.

    Raises:
        CustomHTTPException: If the user does not exist or if there is an error during the deletion process.
    """
    try:
        # Find the existing user
        existing_user = db.query(User).filter(User.id == user_id).first()
        if existing_user is None:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the provided ID does not exist.",
                exception_type="NotFoundError",
                additional_info={"user_id": user_id}
            )

        # Delete the user
        db.delete(existing_user)
        db.commit()
        return existing_user
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while deleting the user from the database.",
            exception_type="DatabaseError",
            additional_info={"error": str(e)}
        )
