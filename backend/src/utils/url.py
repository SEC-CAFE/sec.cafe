#!/usr/bin/env python
# encoding: utf-8

import random
from src.models.url import TUrl
from src.models import api_redis


class TinyURL(object):
    @classmethod
    def generate_random_string(cls):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_string = ''

        for _ in range(4):
            random_char = random.choice(chars)
            random_string += random_char

        return random_string

    @classmethod
    async def shorten(cls, url):
        # 生成短连接码并存储数据库和缓存
        # return 4位随机字符串
        if not url.startswith(('https://', 'http://')):
            return None

        url_code = None
        url_obj = TUrl.get_or_none(url=url)
        if url_obj:
            url_code = url_obj.code
            return url_code

        while not url_code:
            url_code = cls.generate_random_string()
            url_obj = TUrl.get_or_none(code=url_code)
            if url_obj:
                url_code = None
            else:
                url_obj = TUrl.create(url=url, code=url_code)

        api_redis.redis.hset('sec_cafe_tinyurls', url_code, url)
        return url_code

    @classmethod
    async def recovery(cls, url_code):
        # 还原原始URL
        if not url_code:
            return None

        o_url = api_redis.redis.hget('sec_cafe_tinyurls', url_code)
        if not o_url:
            url_obj = TUrl.get_or_none(code=url_code)
            o_url = url_obj.url if url_obj else None
            if o_url:
                api_redis.redis.hset('sec_cafe_tinyurls', url_code, o_url)
        return o_url
