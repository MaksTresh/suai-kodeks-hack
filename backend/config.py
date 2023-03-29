import os

from functools import lru_cache
from typing import Optional, TypeVar

from pydantic import BaseSettings, Field, validator

T = TypeVar("T", str, int)


def get_env(name: str, required: bool = False, default: Optional[T] = None) -> T:
    if required and not default:
        default = ...  # type: ignore
    return Field(default, env=name)


class RedisSettings(BaseSettings):
    REDIS_HOST: str = get_env("REDIS_HOST", required=True)
    REDIS_PORT: int = get_env("REDIS_PORT", default=6379, required=True)
    REDIS_USERNAME: str = get_env("REDIS_USERNAME", default='')
    REDIS_PASSWORD: str = get_env("REDIS_PASSWORD", required=True)
    REDIS_DB_NUMBER: int = get_env("REDIS_DB_NUMBER", default=0)
    REDIS_URL: str = ''


class RabbitMQSettings(BaseSettings):
    RABBITMQ_HOST: str = get_env("RABBITMQ_HOST", required=True)
    RABBITMQ_PORT: int = get_env("RABBITMQ_PORT", default=5672, required=True)
    RABBITMQ_USERNAME: str = get_env("RABBITMQ_DEFAULT_USER", required=True)
    RABBITMQ_PASSWORD: str = get_env("RABBITMQ_DEFAULT_PASS", required=True)
    RABBITMQ_URL: str = ''


class CelerySettings(BaseSettings):
    CELERY_RESULT_EXPIRES: int = 60 * 60
    CELERY_IMPORTS: tuple[str] = (
        "apps.analyzer.tasks",
    )


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: list[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "https://daubi-stand.ru",
        "https://daubi-stand.ru"
    ]


class Settings(RedisSettings, RabbitMQSettings, CelerySettings, CORSSettings):
    UPLOADED_IMAGES_DIR: str = os.path.join(os.getcwd(), "uploaded_images")


@lru_cache
def get_settings() -> Settings:
    return Settings()
