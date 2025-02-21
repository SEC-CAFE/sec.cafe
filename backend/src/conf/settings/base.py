from enum import Enum

from pydantic import BaseSettings


class AppEnvTypes(Enum):
    prod: str = "prod"  # type: ignore
    dev: str = "dev"  # type: ignore
    test: str = "test"  # type: ignore


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod

    class Config:
        env_file = ".envs/.env"
