# -*- coding: utf-8 -*-

"""Definition of the redis locking backend."""

from __future__ import absolute_import

import time
import base64
import datetime
from urllib.parse import urlparse, parse_qsl


def parse_url(url):
    """
    Parse the argument url and return a redis connection.
    Three patterns of url are supported:

        * redis://host:port[/db][?options]
        * redis+socket:///path/to/redis.sock[?options]
        * rediss://host:port[/db][?options]

    A ValueError is raised if the URL is not recognized.
    """
    parsed = urlparse(url)
    kwargs = parse_qsl(parsed.query)

    # TCP redis connection
    if parsed.scheme in ['redis', 'rediss']:
        details = {'host': parsed.hostname}
        if parsed.port:
            details['port'] = parsed.port
        if parsed.password:
            details['password'] = parsed.password
        db = parsed.path.lstrip('/')
        if db and db.isdigit():
            details['db'] = int(db)
        if parsed.scheme == 'rediss':
            details['ssl'] = True

    # Unix socket redis connection
    elif parsed.scheme == 'redis+socket':
        details = {'unix_socket_path': parsed.path}
    else:
        raise ValueError('Unsupported protocol %s' % (parsed.scheme))

    # Add kwargs to the details and convert them to the appropriate type, if needed
    details.update(kwargs)
    if 'socket_timeout' in details:
        details['socket_timeout'] = float(details['socket_timeout'])
    if 'db' in details:
        details['db'] = int(details['db'])

    return details


redis = None


def get_redis(redis_url):
    global redis
    if not redis:
        try:
            from redis import StrictRedis
        except ImportError:
            raise ImportError(
                "You need to install the redis library in order to use Redis"
                " backend (pip install redis)")
        redis = StrictRedis(**parse_url(redis_url), decode_responses=True)
        return redis
    else:
        current_connection_db = redis.connection_pool.connection_kwargs.get('db', 0)
        _parse_url = parse_url(redis_url)
        ready_to_connect_db = _parse_url.get('db')
        if ready_to_connect_db == current_connection_db:
            return redis
        else:
            try:
                from redis import StrictRedis
            except ImportError:
                raise ImportError(
                    "You need to install the redis library in order to use Redis"
                    " backend (pip install redis)")
            new_redis = StrictRedis(**parse_url(redis_url), decode_responses=True)
            return new_redis


class Redis(object):

    def __init__(self, redis_url, run_task_key: str = 'scheduler_task_runing_task'):
        self._redis = get_redis(redis_url)
        self.run_task_key = run_task_key

    @property
    def redis(self):
        return self._redis

    def if_task_running(self, url):
        '''
        查询当前是否执行中，执行中就不重复执行
        '''
        url = str(base64.b64encode(url.encode(encoding="utf-8")), 'utf-8')
        key = f'{self.run_task_key}-{url}'
        exists_key = self._redis.get(key)
        if not exists_key:
            return False
        else:
            return True

    def set_running_task_tag(self, url):
        url = str(base64.b64encode(url.encode(encoding="utf-8")), 'utf-8')
        now = datetime.datetime.now()
        key = f'{self.run_task_key}-{url}'
        self._redis.set(key, str(now))
        self._redis.expire(key, 60*55)

    def delete_complate_task_tag(self, url):
        if url:
            url = str(base64.b64encode(url.encode(encoding="utf-8")), 'utf-8')
            key = f'{self.run_task_key}-{url}'
            self._redis.delete(key)

    def check_and_set_task_run_time(self, task_name, interval_hours=1):
        task_name = str(base64.b64encode(task_name.encode(encoding="utf-8")), 'utf-8')
        key = f'runing_task_time-{task_name}'
        _time = self._redis.get(key)
        if _time:  # 未过时间周期
            return False
        else:
            now = datetime.datetime.now()
            self._redis.set(key, str(now))
            self._redis.expire(key, 60*60*int(interval_hours))  # 为本次执行设置时间
            return True

    def get_request_times(self, username, api_name='api'):
        # 获取用户请求次数
        nwo_str = datetime.datetime.now().strftime('%Y-%m-%d')
        key = f'sec_cafe_api_limit_{api_name}_{nwo_str}'
        request_num = self._redis.hget(key, username)
        if not request_num:
            request_num = 0
        request_num = int(request_num)
        return request_num

    def set_request_times(self, username, api_name='api'):
        # 设置用户已请求次数
        nwo_str = datetime.datetime.now().strftime('%Y-%m-%d')
        key = f'sec_cafe_api_limit_{api_name}_{nwo_str}'
        request_num = self.get_request_times(username, api_name)
        request_num += 1
        key_exists = self._redis.exists(key)

        self._redis.hset(key, username, request_num)
        if not key_exists:
            self._redis.expire(key, 60*60*24)

    def set_access_token(self, token, _time, username):
        # 设置已生成的Token(2倍时间)
        key = 'sec_cafe_access_token'
        value = f'{_time}<|>{username}'
        self._redis.hset(key, token, value)

    def check_access_token(self, token):
        # 检查token有效性
        key = 'sec_cafe_access_token'
        value = self._redis.hget(key, token)
        if not value:
            return False

        _time, username = value.split('<|>', 1)
        now = time.time()
        if float(_time) > now:
            return username
        else:
            self._redis.hdel(key, token)
            return False

    def get_or_set_pusher_id(self, id=None):
        key = 'sec_cafe_vuli_push_last_id'
        if not id:
            id = self._redis.get(key)
            id = int(id) if id else 0
            return id
        else:
            self._redis.set(key, id)

    def get_or_set_pusher_status(self, set=False):
        key = 'sec_cafe_vuli_push_status'
        if not set:
            return self._redis.get(key)
        else:
            self._redis.set(key, str(datetime.datetime.now()))

    def delete_pusher_status(self):
        key = 'sec_cafe_vuli_push_status'
        self._redis.set(key, '')

    def get_or_set_crawler_task(self, url, delete=False):
        key = 'sec_cafe_vuli_crawler_tasks'
        url = str(base64.b64encode(url.encode(encoding="utf-8")), 'utf-8')
        if delete:
            self._redis.hdel(key, url)
        else:
            self._redis.hset(key, url, str(datetime.datetime.now()))

    def check_crawler_task(self):
        key = 'sec_cafe_vuli_crawler_tasks'
        length = self._redis.hlen(key)
        return length == 0
