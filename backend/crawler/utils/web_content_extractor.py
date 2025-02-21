#!/usr/bin/env python
# encoding: utf-8

"""
基于配置的YAML文件提取网页内容，构造json数据结构
"""
import re
from typing import Union
from pyquery import PyQuery as pq
from pyquery.pyquery import PyQuery
from urllib.parse import urljoin


class WebContentExtractor(object):
    def __init__(self, url: str, url_fields: list = ['url'],
                 array_fields: list = ['reference_links', 'cwes', 'components', 'tags']):
        self.array_fields = array_fields  # 数组字段
        self.url = url  # baseurl
        self.url_fields = url_fields  # url字段

    def _value_format(self, selector_key: str, value: Union[list, str]) -> str:
        """将取值格式化处理"""

        # 非数组字段，值为list则进行拼接
        if selector_key not in self.array_fields:
            if isinstance(value, list):
                value = [v for v in value if v]
                value = ''.join(value)
        else:
            # 数组字段，值不为list，则进行构造
            if selector_key in self.array_fields and not isinstance(value, list):
                value = [value] if value else []
            # 如果是数组字段则去重
            value = list(set(value))

        # URL字段处理
        if selector_key in self.url_fields and not value.startswith(('http://', 'https://')):
            value = urljoin(self.url, value)

        return value

    def _value_handler(self, selector_key: str, selector_dict: dict, value: dict) -> dict:
        """针对值进行处理"""

        _map = selector_dict.get('map')
        _break_keywords = tuple(selector_dict.get('break_keyword', []))
        _exists_map = selector_dict.get('exists_map')
        _choise_one = selector_dict.get('choise_one')
        _split_tag = selector_dict.get('split_tag')
        _build = selector_dict.get('build')
        _choise_value_one = selector_dict.get('choise_value_one')
        _value_index = selector_dict.get('value_index')
        _clean_html_tag = selector_dict.get('clean_html_tag')
        _regx = selector_dict.get('regx')

        new_value = {}
        for _key, _value in value.items():
            if _regx and _value:
                result = re.search(_regx, _value, re.I)
                if result:
                    _value = result.group(1)
                else:
                    _value = ''

            if _break_keywords:  # 内容有截断处理
                if isinstance(_value, list):
                    new_value_list = []
                    for _ in _value:
                        if _.startswith(_break_keywords):
                            break
                        else:
                            new_value_list.append(_)
                    _value = new_value_list
                elif isinstance(_value, str):
                    for _break_word in _break_keywords:
                        if _break_word in _value:
                            _value = _value.split(_break_word, 1)[0]
                            break

            if _split_tag:  # 存在分割标记
                _value = _value.split(_split_tag) if _value else []

            if _choise_value_one and isinstance(_value, list):  # 存在取唯一值的标记
                for _v in _value:
                    if _v:
                        _value = _v
                        break

            if _value_index and isinstance(_value, list):
                try:
                    _value = _value[int(_value_index) - 1]
                except Exception:
                    pass

            if _map and isinstance(_value, str):  # 值有映射处理
                _value = _map.get(_value)

            if _exists_map:  # 是否通过值存在与否进行map，如果不为空则取值，排列后面字段覆盖值
                if _key in _exists_map:
                    map_values = _exists_map.get(_key, '').split('<|>')
                    if len(map_values) == 2:
                        _value = map_values[0] if _value else map_values[1]

            if _build:  # 值需要再构造
                _value = _build.replace(f'<{_key}>', str(_value))

            if _clean_html_tag:  # 清除网页标签
                regx = '<[/]{0,1}.*?>'
                is_list_tag = isinstance(_value, list)
                if not is_list_tag:
                    _value = [_value]
                _new_value = []
                for _v in _value:
                    _keywords = re.findall(regx, _v, re.I)
                    for _k in list(set(_keywords)):
                        _v = _v.replace(_k, '')
                    _v = _v.replace('\t', '').replace('\r', '')
                    _new_value.append(_v)
                _value = _new_value if is_list_tag else _new_value[0]

            _value = self._value_format(selector_key, _value)  # 对dict中的值值进行格式化处理
            new_value[_key] = _value

        # 整个value处理逻辑
        value = new_value
        if len(value) == 1 and list(value.keys())[0] == selector_key:  # 单个key，直接取对应值
            value = value[selector_key]
        else:
            if _choise_one:  # 多个key的情况下，按顺序取第一个不为空的值
                new_value = ''
                for sub_key, sub_value in value.items():
                    if sub_value:
                        new_value = sub_value
                        break
                value = new_value
            else:
                value = ''.join(value.values())

        return value

    def _extractor_element_value(self, el: PyQuery, value_attr: str) -> str:
        """取页面元素的值"""

        values = []
        if value_attr == 'textAll':
            values = [el.text().strip()]
        else:
            for _e in el:
                if value_attr == 'text':
                    value = _e.text
                    value = value.strip() if value else value
                elif value_attr == 'textContent':
                    value = _e.text_content().strip()
                    if not value:
                        value = _e.text.strip()
                else:
                    value = _e.get(value_attr)
                values.append(value)
        if len(values) == 1:
            values = values[0]
        return values

    def _extractor_json_value(self, data: Union[dict, list], selector: str, default_value: str = ''):
        def _get_child_value(_data, _selector):
            if '<|>' in _selector:  # 多个字段组合的情况
                value = {}
                for child_selector in _selector.split('<|>'):
                    value[child_selector] = _data.get(child_selector, default_value)
                return value
            elif '?' in _selector:  # 存在条件语句，如value?label=CVSS 3.X
                selector_key, condition = _selector.split('?', 1)
                condition_field, condition_value = condition.split('=', 1)
                if _data.get(condition_field) == condition_value:
                    return _data.get(selector_key, default_value)
                else:
                    return default_value
            else:
                return _data.get(_selector, default_value) if _data else default_value

        if not data:
            return None

        if '/' in selector:
            keys = selector.split('/', 1)
            # if keys[1].startswith('['):  # 是个list字段
            #     return self._extractor_json_value(data.get(keys[0], []), keys[1].replace('[', '').replace(']', ''))  # 去掉[]
            # else:
            #     return self._extractor_json_value(data.get(keys[0], {}), keys[1])
            hand_key = keys[0]
            if hand_key.endswith(']') and hand_key.startswith('[') and isinstance(data, list):
                hand_index = int(hand_key[1:-1])
                hand_data = data[hand_index]
            else:
                hand_data = data.get(hand_key, {})
            return self._extractor_json_value(hand_data, keys[1])
        else:
            if isinstance(data, list):
                values = []
                for _d in data:
                    _value = _get_child_value(_d, selector)
                    values.append(_value)

                if '?' in selector:  # 如果存在条件语句，则取第一个不为空的值
                    new_value = ''
                    for value in values:
                        if value:
                            new_value = value
                            break
                    return new_value
                else:
                    return values
            else:
                return _get_child_value(data, selector)

    def html_extractor(self, root_el: Union[PyQuery, str], _selectors: dict) -> dict:
        """提取HTML页面内容构建dict"""

        data = {}
        if isinstance(root_el, str):
            root_el = pq(root_el)

        for selector_key, _ in _selectors.items():
            el_selector = _['selector']

            if el_selector.startswith('@'):  # 固定值
                data[selector_key] = el_selector[1:]
            else:
                value_attr = _['value_attr']
                select_el = root_el.find(el_selector)

                value = self._extractor_element_value(select_el, value_attr)
                value = {selector_key: value}
                value = self._value_handler(selector_key, _, value)
                data[selector_key] = value

        return data

    def json_extractor(self, _data: dict, _selectors: dict) -> dict:
        """提取JSON页面内容构建dict"""
        # 根据模板从JSON数据集获取内容
        data = {}
        if _data:
            for selector_key, _ in _selectors.items():
                el_selector = _['selector']
                if el_selector.startswith('@'):  # 固定值
                    data[selector_key] = el_selector[1:]
                else:
                    value = self._extractor_json_value(_data, el_selector)
                    if not isinstance(value, dict):
                        value = {selector_key: value}

                    value = self._value_handler(selector_key, _, value)
                    data[selector_key] = value
        return data
