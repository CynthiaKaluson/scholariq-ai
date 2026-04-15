from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ScholarIQ"
    database_url: str
    openai_api_key: str
    api_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
