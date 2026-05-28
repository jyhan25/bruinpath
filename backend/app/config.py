from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bruinpath"
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
