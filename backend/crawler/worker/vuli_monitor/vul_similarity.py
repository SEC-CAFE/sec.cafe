#!/usr/bin/env python
# encoding: utf-8

import openai
import datetime
import macropodus
from crawler.utils.content_utils import replace_keyword
from src.conf.config import get_app_settings

settings = get_app_settings()
openai.api_key = settings.openapi_key


def _get_vul_time(exists_vul: dict, new_vul: dict):
    exists_vul_publish_time = exists_vul.get('publish_time')
    exists_vul_update_time = exists_vul.get('update_time')
    new_vul_publish_time = new_vul.get('publish_time')
    new_vul_update_time = new_vul.get('update_time')

    _times = (exists_vul_publish_time, exists_vul_update_time, new_vul_publish_time, new_vul_update_time)
    new_times = ()
    for _t in _times:
        if _t and isinstance(_t, str):
            _t = datetime.datetime.strptime(_t, '%Y-%m-%d')
        new_times = new_times + (_t,)

    return new_times


def if_not_same_vul(exists_vul: dict, new_vul: dict):
    """
    根据确定的规则检查是否明确不是同个漏洞
    """
    # 编号存在，但值不同，则不是同个漏洞
    fields = ['cve', 'cnnvd', 'cnvd']
    result = False
    for _field in fields:
        value_1 = exists_vul.get(_field)
        value_2 = new_vul.get(_field)
        if value_1 and value_2 and value_1 != value_2:
            result = True
            break

    # 同个来源，不同URL，则不是同个漏洞(依赖于不同来源不会重复录入)
    new_source_name = new_vul.get('source', {}).get('name')
    new_url = new_vul.get('url')
    if new_source_name and new_url:
        # 基于当前漏洞源和URL做判断(已存在的漏洞的related_vuls肯定包含自身，不用重复判断)
        exitst_source_name = exists_vul.get('source', {}).get('name')
        exitst_url = exists_vul.get('url')
        if exitst_url and exitst_source_name == new_source_name and exitst_url != new_url:
            return True

    # 取重复漏洞做判断
    related_vuls = exists_vul.get('related_vuls', [])
    for _ in related_vuls:
        _source_name = _.get('source', {}).get('name')
        _url = _.get('url')
        if _url and _source_name == new_source_name and _url != new_url:
            result = True
            break

    return result


def check_by_tag_num(new_vul: dict, model):
    # 根据编号判断是否同个漏洞
    if new_vul.get('cve'):
        hit_vul = model.get_or_none(cve=new_vul['cve'])
    elif new_vul.get('cnnvd'):
        hit_vul = model.get_or_none(cnnvd=new_vul['cnnvd'])
    elif new_vul.get('cnvd'):
        hit_vul = model.get_or_none(cnvd=new_vul['cnvd'])
    else:
        hit_vul = None
    return hit_vul


def check_by_descript_with_openai(exists_vul: dict, new_vul: dict):
    descript1 = exists_vul.get('descript', '').lower()
    descript2 = new_vul.get('descript', '').lower()
    _times = _get_vul_time(exists_vul, new_vul)
    exists_vul_publish_time = _times[0]
    new_vul_publish_time = _times[2]

    if not descript1 or not descript2 or not exists_vul_publish_time or not new_vul_publish_time:
        return False

    if exists_vul_publish_time != new_vul_publish_time:  # 非同一天漏洞不做判断
        return False

    try:
        chat_define = "你作为一个安全工程师，根据我输入的两段内容分别提取关键漏洞描述摘要，请先输出摘要，然后基于输出的摘要判断是否描述的是同个漏洞，只输出判断结果，结果格式：相同 or 不同"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            temperature=0.4,
            top_p=0.9,
            messages=[
                {"role": "system", "content": chat_define},
                {"role": "user", "content": f"“{descript1}”和“{descript2}”"}
            ]
        )
        result = completion.choices[0].message.content
    except Exception:
        import traceback
        traceback.print_exc()
        result = ''
    if '\n' in result:
        result = result.rsplit('\n', 1)[1].strip()
    if result and "不同" in result:
        return False
    else:
        return True


def check_by_title_and_descript(exists_vul: dict, new_vul: dict):
    # 根据标题相似度去重
    exists_vul_title = exists_vul.get('title', '').lower()
    new_vul_title = new_vul.get('title', '').lower()
    exists_vul_title = exists_vul_title.lower() if exists_vul_title else ''
    new_vul_title = new_vul_title.lower() if new_vul_title else ''

    _times = _get_vul_time(exists_vul, new_vul)
    exists_vul_publish_time = _times[0]
    exists_vul_update_time = _times[1]
    new_vul_publish_time = _times[2]
    new_vul_update_time = _times[3]

    if not exists_vul_title or not new_vul_title:
        return False

    if (not exists_vul_publish_time or not new_vul_publish_time) and \
       (not exists_vul_update_time or not new_vul_update_time):
        return False

    # 做关键词替换处理
    exists_vul_title = replace_keyword(exists_vul_title)
    new_vul_title = replace_keyword(new_vul_title)

    # 判断第一个词是否一致
    words1 = list(macropodus.cut(exists_vul_title))
    words2 = list(macropodus.cut(new_vul_title))
    if words1[0] != words2[0]:
        return False

    # 计算相似度
    sents = macropodus.sim(exists_vul_title, new_vul_title, type_sim="total", type_encode="avg")

    # 如果发布/更新日期相差1天内，则相似度要求降低；否则要求较高
    publish_time_offset = -1
    update_time_offset = -1
    if exists_vul_publish_time and new_vul_publish_time:  # 根据发布时间对比
        publish_time_offset = new_vul_publish_time - exists_vul_publish_time
        publish_time_offset = abs(publish_time_offset.days)

    if exists_vul_update_time and new_vul_update_time:  # 根据更新时间对比
        update_time_offset = new_vul_update_time - exists_vul_update_time
        update_time_offset = abs(update_time_offset.days)

    time_offset_check = publish_time_offset in [0, 1] or update_time_offset in [0, 1]

    if (sents > 0.65 and time_offset_check) or sents > 0.9:
        return True
    
    if settings.openapi_key:
        if check_by_descript_with_openai(exists_vul, new_vul):
            return True

    return False


def check_by_reference_links(exists_vul: dict, new_vul: dict):
    # 根据相关链接的包含关系确认是否同个漏洞
    reference_links1 = exists_vul.get('reference_links')
    reference_links2 = new_vul.get('reference_links')
    reference_links1 = [] if not reference_links1 else reference_links1
    reference_links2 = [] if not reference_links2 else reference_links2
    url1 = exists_vul.get('url')
    url2 = new_vul.get('url')

    if (not reference_links1 and not reference_links2) or not url1 and not url2:
        return False

    if (url1 and url1 in reference_links2) or (url2 and url2 in reference_links1):
        return True

    return False


def check_vul_similarity(exists_vul: dict, new_vul: dict):
    """
    多种方式判断是否同个漏洞
    """
    if if_not_same_vul(exists_vul, new_vul):
        return False

    if check_by_reference_links(exists_vul, new_vul):
        return True

    if check_by_title_and_descript(exists_vul, new_vul):
        return True

    return False
