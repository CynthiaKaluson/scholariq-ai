from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Scholariq-AI"
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()