from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "TZ_EFF_MOB"
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30
    ACCESS_TOKEN_TYPE_FIELD: str = "access"
    REFRESH_TOKEN_TYPE_FIELD: str = "refresh"

    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()