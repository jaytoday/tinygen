from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    UPLOAD_FOLDER: str
    SUPABASE_URL: str
    SUPABASE_KEY: str

    def get_db_url(self):
        return self.SUPABASE_URL


settings = Settings()
