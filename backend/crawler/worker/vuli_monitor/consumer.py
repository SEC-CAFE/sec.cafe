#!/usr/bin/env python
# encoding: utf-8

import re
import asyncio
import xmltodict
from celery import signature
from pyquery import PyQuery as pq

from crawler.utils.content_utils import format_html_to_json
from crawler.utils.translate import Translater
from crawler.utils.web_content_extractor import WebContentExtractor
from crawler.scheduler.app import celery_app
from crawler.scheduler.models import task_redis
from crawler.worker.vuli_monitor.recycler import result_handler

from src.utils.req import HttpReq
from src.models import db_object
from src.models.vul_intelligence import OVulIntelligence

from src.conf.config import get_app_settings

settings = get_app_settings()


def _replace_value(field: str, data: dict):
    if not field:
        return field

    if '<' in field and '>' in field:
        key = field.split('<', 1)[1].split('>', 1)[0]
        if key in data:
            field = field.replace(f'<{key}>', str(data[key]))
    return field


def get_url(template: dict, data: dict, _type: str):
    if _type == 'crawl_detail':
        url = template.get('crawl_detail', {}).get('url')
    else:
        url = template.get('crawl_list', {}).get('url')

    url = _replace_value(url, data)
    return url


async def req_html(template: dict, data: dict, url: str, _type: str):
    if _type == 'crawl_detail':
        req_dict = template.get('crawl_detail', {})
    else:
        req_dict = template.get('crawl_list', {})

    httpreq = HttpReq(settings.req_ua)

    # 预请求
    cookie = ''
    pre_req = req_dict.get('pre_req', {})
    if pre_req and pre_req.get('url'):
        html, resp = await httpreq.request(
            pre_req['url'],
            pre_req.get('method', 'get'),
            pre_req.get('params', ''),
            pre_req.get('headers', {}),
            retry_limit=3)
        if resp:
            cookie = resp.cookies.output(header='').strip()

    # 请求主内容
    headers = req_dict.get('headers', {})
    if headers:
        for key, value in headers.items():
            headers[key] = _replace_value(value, data)
    if cookie:
        headers['Cookie'] = cookie

    params = _replace_value(req_dict.get('params', None), data)
    method = req_dict.get('method', 'get')
    html, resp = await httpreq.request(url, method, params, custom_headers=headers, retry_limit=3)
    return html, req_dict


@celery_app.task(name='task.vuli_monitor.crawler_list', ignore_result=True)
def crawler_list(record_id: str, template: dict, debug: bool = False):
    # 获取列表
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_crawler_list(record_id, template, debug))
    loop.run_until_complete(task)


async def _crawler_list(record_id: str, template: dict, debug: bool = False):
    async def create_get_detail_task(data, template):
        fitler_tag = template.get('crawl_list', {}).get('filter', {})
        filter_not_hit = False
        for field, keyword in fitler_tag.items():
            _value = data.get(field)
            if field and keyword and field in data:
                keyword = str(keyword)
                if keyword.startswith('='):
                    keywords = keyword[1:].split(',')
                    if str(_value) not in keywords:
                        filter_not_hit = True
                        break
                elif keyword.startswith('re_'):
                    regx = keyword[3:]
                    result = re.search(regx, _value, re.I)
                    result = result.group() if result else ''
                    if result != _value:
                        filter_not_hit = True
                elif keyword not in _value:
                    filter_not_hit = True
                    break
        if filter_not_hit:
            return

        if debug:
            data = await _crawler_detail(data, template, debug)
            print('---------crawl-data--------')
            print(data)
            await result_handler(data, debug=debug)
        else:
            celery_app.send_task(
                'task.vuli_monitor.crawler_detail',
                args=(data, template),
                chain=[
                    signature('task.result_handler', args=('task.vuli_monitor.crawler_list', record_id, 10))
                ]
            )
    interval_hours = template.get('interval_hours')
    source_name = template['name']
    if interval_hours:
        check_ret = task_redis.check_and_set_task_run_time(source_name, interval_hours)
        if not check_ret:  # 未到下一轮爬取周期
            print(f'未到下一个爬取周期，{source_name}')
            return

    print(f'开始爬取来源：{source_name}')
    url = get_url(template, {}, 'crawl_list')
    WCE = WebContentExtractor(url=url)
    html, req_dict = await req_html(template, {}, url, 'crawl_list')

    list_value_selectors = template['list_value_selectors']
    content_format = req_dict.get('content_format', 'html')

    if not html:
        print(f'爬取失败，{source_name}')
        return

    if content_format == 'html':  # 正常网页内容
        doc = pq(html)
        _list = doc.find(template['list_selector'])
        for _tr in _list.items():
            data = WCE.html_extractor(_tr, list_value_selectors)
            await create_get_detail_task(data, template)
    else:  # json/XML内容
        if content_format == 'xml':
            doc = xmltodict.parse(html.strip(), encoding='utf-8')
        else:
            if_nuxt = req_dict.get('if_nuxt', False)
            doc = format_html_to_json(html, if_nuxt)
        _list = WCE._extractor_json_value(doc, template['list_selector'], [])
        if not isinstance(_list, list):
            _list = [_list]

        sort = template.get('sort')  # 按字段排序
        if sort:
            if sort.startswith('-'):
                sort = sort[1:]
                reverse = True
            else:
                reverse = False
            _list = sorted(_list, key=lambda x: x[sort], reverse=reverse)

        list_limit = template.get('list_limit')  # 是否限制list长度
        if list_limit and int(list_limit) > 0:
            _list = _list[:int(list_limit)]

        for _ in _list:
            if _:
                data = WCE.json_extractor(_, list_value_selectors)
                await create_get_detail_task(data, template)


@celery_app.task(name='task.vuli_monitor.crawler_detail', ignore_result=True)
def crawler_detail(data: dict, template: dict):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_crawler_detail(data, template))
    loop.run_until_complete(task)
    return task.result()


async def _crawler_detail(data: dict, template: dict, debug: bool = False):
    vul_url = data.get('url')

    if not vul_url:
        return None

    if debug:
        task_redis.delete_complate_task_tag(vul_url)

    if task_redis.if_task_running(vul_url):  # 如果执行任务已存在
        return None

    req_url = get_url(template, data, 'crawl_detail')
    WCE = WebContentExtractor(url=req_url)

    with db_object.allow_sync():
        _obj = OVulIntelligence.get_or_none(url=vul_url)
        if _obj and not debug:  # 已经爬取过这个URL
            return None

        detail_value_selectors = template.get('detail_value_selectors')
        if detail_value_selectors:
            task_redis.set_running_task_tag(vul_url)
            html, req_dict = await req_html(template, data, req_url, 'crawl_detail')
            content_format = req_dict.get('content_format', 'html')
            if not html:  # 详情没爬取成功，放弃任务，返回空，等待下次爬取
                return None
            else:
                if content_format == 'html':  # 正常网页内容
                    doc = pq(html)
                    new_data = WCE.html_extractor(doc, detail_value_selectors)
                else:  # json内容
                    if content_format == 'xml':
                        doc = xmltodict.parse(html.strip(), encoding='utf-8')
                    else:
                        if_nuxt = req_dict.get('if_nuxt', False)
                        doc = format_html_to_json(html, if_nuxt)
                    new_data = WCE.json_extractor(doc, detail_value_selectors)

                data.update(new_data)
            task_redis.delete_complate_task_tag(vul_url)
        if data:
            data['source'] = {
                'name': template.get('name'),
                'homepage': template.get('homepage'),
                'priority': int(template.get('priority', 999))
            }
            if template.get('translate', False):
                T = Translater()
                if data.get('title'):
                    new_title = T.translate(data['title'])
                    data['title'] = new_title if new_title else data['title']
                if data.get('descript'):
                    new_descript = T.translate(data['descript'])
                    data['descript'] = new_descript if new_descript else data['descript']
        return data
