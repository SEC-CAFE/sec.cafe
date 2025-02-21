import logging
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger

from src.utils.logging import InterceptHandler
from src.conf.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "SEC.CAFE"
    version: str = "1.0"
    site_url: str = ""

    # db config
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    redis_host: str
    redis_port: int
    redis_password: str

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_ui_port: int

    # other config
    browser_servers: str = ""
    browser_ports: str = ""
    browser_num: int = 0
    browser_token: str = ""

    # translate config
    translate_tencent_id: str = ''
    translate_tencent_key: str = ''
    translate_baidu_id: str = ''
    translate_baidu_key: str = ''
    translate_xiaoniu_key: str = ''

    # sentry config
    sentry_api_dns: str = ''
    sentry_crawler_dns: str = ''
    sentry_backend_dns: str = ''

    # req config
    req_ua: str = ''

    # open api
    openapi_key: str = ''

    secret_key: str = ""
    api_secret_key: str = ""
    api_access_token_expire_minutes: int = 0
    access_token_expire_minutes: int = 0

    api_prefix: str = ""
    # api_prefix: str = "/api"

    # auth
    github_client_id: str = ""
    github_secret: str = ""

    # mail server
    mail_host: str = ""
    mail_port: int = 0
    mail_user: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_bcc: str = ""

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
