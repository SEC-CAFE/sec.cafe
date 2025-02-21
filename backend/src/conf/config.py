from functools import lru_cache
from typing import Dict, Type

from src.conf.settings.app import AppSettings
from src.conf.settings.base import AppEnvTypes, BaseAppSettings
from src.conf.settings.development import DevAppSettings
from src.conf.settings.production import ProdAppSettings
from src.conf.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()  # type: ignore
