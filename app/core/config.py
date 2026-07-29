from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "FraudShield AI"
    app_version: str = "1.0.0"
    api_version: str = "v1"

    host: str = "127.0.0.1"
    port: int = 8000

    log_level: str = "INFO"

    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()