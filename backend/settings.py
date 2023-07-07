from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_PORT: int
    MONGODB_HOST: str

    COOKIES_EXPIRES_IN: int

    SECRET_KEY: str

    class Config:
        env_file = '../.env'


settings = Settings()
