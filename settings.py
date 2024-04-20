from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    LOGS_DIR: Path = Path(__file__).resolve().parent / 'logs'

    WARNING_LOG_FILE_PATH: Path = LOGS_DIR / 'warning.log'

    SECONDS_BLOCKS_LIMIT_BY_USER: int = 25
    REQUEST_MAX_SECONDS: int = 30
    STT_SECONDS_IN_BLOCK: int = 15
    STT_URL: str = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
    STT_LANGUAGE: str = 'ru-RU'

    DB_URL: str
    BOT_TOKEN: str
    STT_API_KEY: str
    STT_FOLDER_ID: str


_SETTINGS = Settings()

_SETTINGS.LOGS_DIR.mkdir(exist_ok=True)


def __getattr__(name: str) -> Any:
    return getattr(_SETTINGS, name)
