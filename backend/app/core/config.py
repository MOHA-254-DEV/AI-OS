import os
from pydantic import BaseSettings, EmailStr, Field, AnyUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-OS Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="DATABASE_URL")

    # Email
    SMTP_HOST: str = Field(..., env="SMTP_HOST")
    SMTP_PORT: int = Field(..., env="SMTP_PORT")
    SMTP_USER: str = Field(..., env="SMTP_USER")
    SMTP_PASSWORD: str = Field(..., env="SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: EmailStr = Field(..., env="SMTP_FROM_EMAIL")
    EMAILS_FROM_NAME: str = "AI-OS"
    EMAILS_ENABLED: bool = True

    # File storage
    FILES_STORAGE: str = Field("local", env="FILES_STORAGE")  # local or s3
    FILES_LOCAL_PATH: str = Field("./app/static/files", env="FILES_LOCAL_PATH")
    S3_BUCKET: str = Field("", env="S3_BUCKET")
    S3_REGION: str = Field("", env="S3_REGION")
    S3_ACCESS_KEY: str = Field("", env="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field("", env="S3_SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
