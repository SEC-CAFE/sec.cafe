#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlencode
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Optional, Union

from playwright.async_api import Browser as PBrowser
from playwright.async_api import BrowserContext, async_playwright


class Browser(object):
    _redis_counter_initialized = False

    def __init__(self, browser_urls: list, redis=None):
        self.browser_load = {}
        self.requests = {}
        self.redis = redis
        self.urls = browser_urls
        self.redis_key = 'browser_req_count'

        if self.redis:
            # 在进程生命周期内初始化一次计数器，避免每次请求清空并发计数。
            if not Browser._redis_counter_initialized:
                for url in self.urls:
                    if self.redis.hget(self.redis_key, url) is None:
                        self.redis.hset(self.redis_key, url, 0)
                Browser._redis_counter_initialized = True
        else:
            for url in self.urls:
                self.browser_load[url] = 0

    def _get_browser_url(self):
        browser_url = None
        min_open_num = 1_000_000
        for url in self.urls:
            if self.redis:
                num = self.redis.hget(self.redis_key, url)
                num = int(num) if num else 0
            else:
                num = self.browser_load[url]
            if num < min_open_num:
                min_open_num = num
                browser_url = url

        if not browser_url:
            return ''

        if self.redis:
            self.redis.hset(self.redis_key, browser_url, min_open_num + 1)
        else:
            self.browser_load[browser_url] += 1
        return browser_url

    async def _close_browser(self, browser, context, page, browser_url):
        try:
            await page.close()
            await context.close()
            await browser.close()
        except Exception:
            pass

        if self.redis and browser_url:
            num = self.redis.hget(self.redis_key, browser_url)
            num = int(num) if num else 0
            num = num - 1 if num > 0 else 0
            self.redis.hset(self.redis_key, browser_url, num)
        elif browser_url:
            self.browser_load[browser_url] = max(0, self.browser_load[browser_url] - 1)

    @asynccontextmanager
    async def _get_new_context(
        self,
        browser: PBrowser,
        headers: Optional[Dict] = None,
        cookies: Union[list, dict, None] = None,
        proxy: Optional[dict] = None,
        **kwargs,
    ) -> AsyncGenerator[BrowserContext, None]:
        kwargs['extra_http_headers'] = headers
        if proxy:
            kwargs['proxy'] = proxy

        context = await browser.new_context(**kwargs)

        if cookies and isinstance(cookies, dict):
            cookies = [{'name': key, 'value': value} for key, value in cookies.items()]
        if cookies:
            await context.add_cookies(cookies)

        yield context

    def _request_handler(self, request, page_id):
        if request.method == 'POST':
            self.requests[page_id] = request

    async def get(
        self,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[Dict] = None,
        cookies: Union[list, dict, None] = None,
        proxy: Optional[dict] = None,
        timeout: int = 60000,
        get_wait_for_selector: Optional[str] = None,
        **kwargs,
    ):
        if params:
            params_url_string = urlencode(params)
            url = f'{url}?{params_url_string}'

        browser_url = self._get_browser_url()
        if not browser_url:
            return None, {'content': '', 'headers': {}, 'cookies': []}

        async with async_playwright() as playwright:
            browser = await playwright.chromium.connect_over_cdp(browser_url)
            async with self._get_new_context(browser, headers, cookies, proxy, **kwargs) as context:
                page = await context.new_page()
                try:
                    resp = await page.goto(url, timeout=timeout, wait_until="load")
                    if get_wait_for_selector:
                        await page.locator(get_wait_for_selector).wait_for()

                    page_headers = resp.headers if resp else {}
                    page_cookies = await context.cookies()
                    content = await page.content()
                    if not content:
                        content = await page.evaluate('document.documentElement.innerHTML')

                    return resp, {
                        'content': content,
                        'headers': page_headers,
                        'cookies': page_cookies,
                    }
                finally:
                    await self._close_browser(browser, context, page, browser_url)
