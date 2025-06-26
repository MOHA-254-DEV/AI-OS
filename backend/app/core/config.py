import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    FILES_STORAGE: str = "local"  # or "s3"
    FILES_LOCAL_PATH: str = "./data/files"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = ""
    S3_REGION: str = ""

    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_TLS: bool = True

    PROJECT_NAME: str = "AI-OS"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
