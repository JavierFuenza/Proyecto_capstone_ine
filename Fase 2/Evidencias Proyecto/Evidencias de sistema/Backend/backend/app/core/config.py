import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "")

    # API Info
    api_name: str = "Observatorio Ambiental Backend"
    api_version: str = "0.1.0"
    api_description: str = "API para datos ambientales de Chile"

    # CORS
    allowed_origins: list = [
        "https://observatorio.javierfuenzam.com",
        "http://localhost:4321",  # Desarrollo local
    ]
    allowed_methods: list = ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: list = ["*"]

    # Contact Info
    contact_email: str = "contacto@observatorio.cl"

    class Config:
        env_file = ".env"

settings = Settings()