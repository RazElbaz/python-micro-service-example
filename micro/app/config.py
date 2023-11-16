from pydantic_settings import BaseSettings
from logging import INFO, DEBUG, ERROR, WARNING

class Settings(BaseSettings):
    DATABASE_URL: str
    # MONGO_INITDB_DATABASE: str

    # JWT_PUBLIC_KEY: str
    # JWT_PRIVATE_KEY: str
    # REFRESH_TOKEN_EXPIRES_IN: int
    # ACCESS_TOKEN_EXPIRES_IN: int
    # JWT_ALGORITHM: str
    # CLIENT_ORIGIN: str

    CORS_ORIGINS: list[str] = ["*"]
    LOG_LEVEL: int = INFO
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 90


    class Config:
        env_file = '.env'
        

settings = Settings()

