#!/usr/bin/env python
# encoding: utf-8

import re
import json
import js2py

from json.decoder import JSONDecodeError
from pyquery import PyQuery as pq


KEYWORDS_MAP = {
    'weaver': '泛微',
    'tencent企业微信': '企业微信',
    'ZenTao PMS': '禅道',
    '普元 EOS': 'Primeton EOS'
}


def format_html_to_json(html, if_nuxt=False):
    if if_nuxt:  # 如果nuxt框架，需要执行js
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
            html = {'data': data}

    if isinstance(html, dict):
        doc = html
    else:
        try:
            doc = json.loads(html)
        except JSONDecodeError:
            doc = None
    return doc


def remove_no_exists_field(model, data: dict):
    keys = model._meta.fields.keys()
    new_data = {}
    for key, value in data.items():
        if key in keys:
            new_data[key] = value
    return new_data


def clean_title(title, data):
    keywords = (
        '的安全通告',
        '安全通告',
        '漏洞通告',
        '通告'
    )
    tag_keywords = ['【】', '()', '（）', '[]', '""', '：']
    if title:
        '''
        keys = ['tag_num', 'cve', 'cnnvd', 'cnvd']
        for _k in keys:
            values = data.get(_k)
            if values:
                if isinstance(values, str):
                    values = [values]
                for _v in values:
                    result = re.findall('({}[,、;；,]?)'.format(_v), title, re.I)
                    if result:
                        title = title.replace(result[0], '').replace('()', '').replace('（）', '')
        '''

        result = re.search(r'([\(（](?:[a-z]*-\d{1,5}-\d{1,10}[,、;；,/]*?)+[\)）])', title, re.I)
        if result:
            title = title.replace(result.group(1), '')

        regx = r'[\(\[（【“"][,、;；,]+[\)\]）】”"]'
        result = re.search(regx, title, re.I)
        if result:
            title = title.replace(result.group(), '')

        for keyword in keywords:
            if keyword in title:
                title = title.replace(keyword, '')

        for keyword in tag_keywords:
            title = title.replace(keyword, '')

    return title


def get_cve_cnvd_and_cnnvd(data):
    title = data.get('title')
    if title:
        result = re.findall(r'((?:CVE|CNNVD|CNVD)-\d{4,6}-\d{3,6})', title, re.I)
        for _r in result:
            _r = _r.upper()
            if _r.startswith('CVE') and not data.get('cve'):
                data['cve'] = _r
            elif _r.startswith('CNNVD') and not data.get('cnnvd'):
                data['cnnvd'] = _r
            elif _r.startswith('CNVD') and not data.get('cnvd'):
                data['cnvd'] = _r
        # data['title'] = title
        title = clean_title(title, data)
    return data, title


def replace_keyword(content):
    content_lower = content.lower()
    content_lower = content_lower.replace(' ', '')
    for key, value in KEYWORDS_MAP.items():
        if key in content_lower:
            _index = content_lower.index(key)
            replace_keyword = content[_index:_index + len(key)]
            content = content.replace(replace_keyword, value)
    return content
