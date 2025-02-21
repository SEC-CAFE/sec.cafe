#!/usr/bin/env python
# encoding: utf-8

import os
import yaml
import copy
import datetime
from sentry_sdk import capture_exception
from playhouse.shortcuts import dict_to_model, model_to_dict

from src.utils.url import TinyURL
from src.models import db_object
from src.models.vul_intelligence import OVulIntelligence, VulIntelligence
from crawler.utils.content_utils import get_cve_cnvd_and_cnnvd, remove_no_exists_field
from crawler.worker.vuli_monitor.vul_similarity import check_vul_similarity, check_by_tag_num


def rectify_value(data):
    float_fiels = ['cvss', 'custom_score', 'level']
    for _field in float_fiels:
        _value = getattr(data, _field)
        if not isinstance(_value, (int, float)):
            _value = None
            setattr(data, _field, _value)
    return data


def update_vul(o_vul: VulIntelligence, new_vul: dict):
    # 去重漏洞字段值合并到存在漏洞
    str_fields = ['descript', 'cve', 'cnnvd', 'cnvd', 'vul_category', 'poc_status', 'cvss', 'level', 'patch']
    list_fields = ['components', 'cwes', 'reference_links', 'tags']

    for _field in str_fields:
        old_value = getattr(o_vul, _field)
        new_value = new_vul.get(_field)
        if not old_value and new_value:
            setattr(o_vul, _field, new_value)

    for _field in list_fields:
        old_value = getattr(o_vul, _field)
        if not old_value:
            old_value = []
        new_value = new_vul.get(_field, [])
        if new_value:
            if not isinstance(new_value, list):
                new_value = [new_value]
            old_value.extend(new_value)
            setattr(o_vul, _field, list(set(old_value)))

    # 特殊处理去重逻辑
    url = o_vul.url
    reference_links = o_vul.reference_links
    if url and reference_links and url in reference_links:
        reference_links.remove(url)
        o_vul.reference_links = reference_links

    return o_vul


def build_vul(hit_vul, data, title, debug=False):
    # 构建入库漏洞内容
    if not hit_vul:
        hit_vul = dict_to_model(VulIntelligence, data)
        hit_vul.title = title
        related_vuls = []
    else:
        related_vuls = copy.deepcopy(hit_vul.related_vuls)
        # 如果优先级比较高，则替换主体内容
        o_vul_priority = data.get('source', {}).get('priority', 999) if data.get('source', {}) else 999
        hit_vul_priority = hit_vul.source.get('priority', 999)
        if o_vul_priority < hit_vul_priority:
            o_id = hit_vul.id
            hit_vul = dict_to_model(VulIntelligence, data)
            hit_vul.title = title
            hit_vul.id = o_id

        hit_vul = update_vul(hit_vul, data)  # 更新最终漏洞的字段
    hit_vul = rectify_value(hit_vul)

    # 更新相关漏洞信息
    is_in_related = False
    for _ in related_vuls:
        if _['url'] == data['tinyurl']:
            is_in_related = True
            break
    if not is_in_related:
        related_vuls.append(
            {
                'title': data['title'],
                'url': data['tinyurl'],
                'source': data.get('source', {})
            }
        )
    hit_vul.related_vuls = related_vuls
    if len(related_vuls) > 1:
        hit_vul.multiple_source = True
    hit_vul.update_time = datetime.datetime.now()
    if debug:
        print('---------result-handler-data--------')
        print(model_to_dict(hit_vul))
    else:
        hit_vul.save()


async def result_handler(data: dict, refresh: bool = False, debug: bool = False):
    # 结果处理函数，保存结果到数据库里
    if data:
        try:
            data = remove_no_exists_field(VulIntelligence, data)
            hit_vul = None
            data, title = get_cve_cnvd_and_cnnvd(data)
            # 特殊情况处理，fix 保存报错
            if not data.get('patch'):
                data['patch'] = False
            if data.get('level') == '':
                data['level'] = None

            with db_object.allow_sync():
                if not data.get('tinyurl') and data.get('url'):
                    data['tinyurl'] = await TinyURL.shorten(data['url'])
                o_vul = OVulIntelligence.get_or_none(url=data['url'])
                if not o_vul or refresh:  # 强制刷新或者新漏洞，避免重复入库
                    if not o_vul and not debug:  # 源漏洞不存在则保存
                        o_vul = dict_to_model(OVulIntelligence, data)
                        o_vul = rectify_value(o_vul)
                        o_vul.save()
                        data['update_time'] = datetime.datetime.now()

                    hit_vul = check_by_tag_num(data, VulIntelligence)  # 基于漏洞编号判断是否一致

                    if not hit_vul:
                        publish_time = data['publish_time']
                        if publish_time:
                            if isinstance(publish_time, str):
                                publish_time = publish_time[:10]
                                data['publish_time'] = publish_time
                                publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d')
                            day_befor_2 = publish_time - datetime.timedelta(days=5)
                            day_befor_2 = datetime.datetime.combine(day_befor_2, datetime.time())
                            vuls = VulIntelligence.select().where(VulIntelligence.publish_time >= day_befor_2)
                            for _v in vuls:
                                if _v.url == data['url']:
                                    continue

                                exists_vul = model_to_dict(_v)
                                if check_vul_similarity(exists_vul, data):  # 检测是否同个漏洞
                                    hit_vul = _v
                                    break

                    build_vul(hit_vul, data, title, debug)  # 更新保存漏洞
        except Exception as err:
            import traceback
            traceback.print_exc()
            capture_exception(err)
            return {'error': 'save db data error'}
        else:
            return {'result': 'save success'}
    else:
        return {'error': 'data is null'}


def args_handler():
    # 参数处理函数，获取所有模板作为任务参数
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(current_file_path, 'templates')

    args = []
    for _ in os.listdir(templates_path):
        file_path = os.path.join(templates_path, _)
        if os.path.isfile(file_path) and _.endswith('.yml'):
            with open(file_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                args.append(data)
    return args
