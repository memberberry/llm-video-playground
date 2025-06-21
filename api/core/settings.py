from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# read version
with open("api/core/VERSION", "r") as f:
    VERSION = f.read().strip()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    LOG_LEVEL: str
    VERSION: str = VERSION
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

if settings.LOG_LEVEL == "DEBUG":
    settings.LOG_LEVEL = logging.DEBUG
elif settings.LOG_LEVEL == "INFO":
    settings.LOG_LEVEL = logging.INFO
elif settings.LOG_LEVEL == "WARNING":
    settings.LOG_LEVEL = logging.WARNING
elif settings.LOG_LEVEL == "ERROR":
    settings.LOG_LEVEL = logging.ERROR
elif settings.LOG_LEVEL == "CRITICAL":
    settings.LOG_LEVEL = logging.CRITICAL
else:
    raise ValueError(f"Invalid LOG_LEVEL: {settings.LOG_LEVEL}")