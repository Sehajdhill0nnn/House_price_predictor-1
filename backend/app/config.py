from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./house_prices.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_dir: str = "backend/trained_models"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def model_path(self) -> Path:
        path = Path(self.model_dir)
        if path.is_absolute():
            return path
        return (Path(__file__).resolve().parents[2] / path).resolve()

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
