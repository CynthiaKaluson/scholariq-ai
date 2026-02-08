from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Scholariq-AI"
    environment: str = "development"
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
