#!/usr/bin/env python
# encoding: utf-8

import pathmagic # noqa
import js2py
import asyncio
from pyquery import PyQuery as pq
from src.utils.req import HttpReq


async def crawl():
    httpreq = HttpReq()
    url = 'https://ti.dbappsecurity.com.cn/vul?page=1'
    html, resp = await httpreq.request(url, 'get')
    doc = pq(html)
    scripts = doc.find('script')

    script_content = ''
    for _s in scripts:
        script_content = _s.text
        if script_content and script_content.startswith('window.__NUXT__='):
            break

    if script_content:
        data = js2py.eval_js(script_content)
        data = data.to_dict()
        data = data.get('ssrRefs', {})
        for key, value in data.items():
            if isinstance(value, list):
                data = value
                break
        print(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(crawl())

    loop.run_until_complete(task)
