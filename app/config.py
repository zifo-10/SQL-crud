from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description='Database URL')

    # Optional: You can add other environment variables here
    class Config:
        env_file = ".env"  # Specify the .env file location if needed


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# This will load settings from the .env file and make it available
setting_loader = get_settings()
