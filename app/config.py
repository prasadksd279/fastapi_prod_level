from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None

    db_host: str | None = None
    db_port: str | None = None
    db_pass: str | None = None
    db_name: str | None = None
    db_uname: str | None = None

    secret_key: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
