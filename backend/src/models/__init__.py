#!/usr/bin/env python
# encoding: utf-8

from src.utils.db import gen_db
from src.utils.redis import Redis
from src.conf.config import get_app_settings


settings = get_app_settings()
# db, db_object = gen_db_by_url(settings.database_url)


main_db_config = {
    'host': settings.postgres_host,
    'port': settings.postgres_port,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'database': settings.postgres_db
}
db, db_object = gen_db(main_db_config)


redis_uri = 'redis://:{}@{}:{}/2'.format(
    settings.redis_password,
    settings.redis_host,
    settings.redis_port
)
api_redis = Redis(redis_uri)

browser_urls = []
if settings.browser_ports:
    start_port = int(settings.browser_ports.split('-')[0])
    browser_post = [start_port + n for n in range(0, settings.browser_num)]
    for ip in settings.browser_servers.split(','):
        for port in browser_post:
            browser_urls.append(f'ws://{ip}:{port}?token={settings.browser_token}')
