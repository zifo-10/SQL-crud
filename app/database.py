from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import setting_loader

# Database configuration
DATABASE_URL = setting_loader.DATABASE_URL

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base for SQLAlchemy models
Base = declarative_base()
