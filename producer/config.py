from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
class Settings(BaseSettings):
    RABBIT_HOST: str
    RABBIT_PORT: str
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str

# Create an instance of the Settings class
settings = Settings()
