from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_app_settings() -> AppSettings:
    return AppSettings()
