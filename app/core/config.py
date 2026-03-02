from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Scholariq-AI"
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env


settings = Settings()