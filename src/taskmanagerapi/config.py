# src/taskmanagerapi/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str = "changeme"  # placeholder, real value comes later in Milestone 2

    class Config:
        env_file = ".env"

settings = Settings()