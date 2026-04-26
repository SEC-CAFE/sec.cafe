#!/usr/bin/env python
# encoding: utf-8

import openai
import json
import datetime
import macropodus
from crawler.utils.content_utils import replace_keyword
from src.conf.config import get_app_settings

settings = get_app_settings()

DEFAULT_OPENAI_MODEL = 'gpt-4o-mini'
DEFAULT_AI_PROMPT = (
    "你是安全漏洞去重助手。根据输入的两条漏洞数据，判断是否描述同一漏洞。"
    "仅输出JSON，不要输出其他文本。格式："
    "{\"same\": true/false, \"confidence\": 0-1之间小数, \"reason\": \"一句中文理由\"}。"
    "若证据不足请返回 same=false 且 confidence<=0.5。"
)


def _parse_time(value):
    if not value:
        return value
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime.combine(value, datetime.time.min)
    if isinstance(value, str):
        value = value.strip()
        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d', '%Y/%m/%d %H:%M:%S'):
            try:
                return datetime.datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def _get_vul_time(exists_vul: dict, new_vul: dict):
    exists_vul_publish_time = exists_vul.get('publish_time')
    exists_vul_update_time = exists_vul.get('update_time')
    new_vul_publish_time = new_vul.get('publish_time')
    new_vul_update_time = new_vul.get('update_time')

    _times = (exists_vul_publish_time, exists_vul_update_time, new_vul_publish_time, new_vul_update_time)
    new_times = ()
    for _t in _times:
        _t = _parse_time(_t)
        new_times = new_times + (_t,)

    return new_times


def _day_offset(day1, day2, default=-1):
    if not day1 or not day2:
        return default
    return abs((day2 - day1).days)


def _normalize_text(value: str, max_len: int):
    if not value:
        return ''
    value = value.strip().replace('\r', ' ').replace('\n', ' ')
    return value[:max_len]


def _build_ai_payload(vul: dict):
    max_len = max(200, settings.vul_similarity_ai_max_desc_len)
    return {
        "title": _normalize_text(vul.get('title', ''), 300),
        "descript": _normalize_text(vul.get('descript', ''), max_len),
        "cve": vul.get('cve') or '',
        "cnnvd": vul.get('cnnvd') or '',
        "cnvd": vul.get('cnvd') or '',
        "url": vul.get('url') or '',
        "source": vul.get('source', {}).get('name', ''),
        "publish_time": vul.get('publish_time') or '',
        "update_time": vul.get('update_time') or '',
    }


def _parse_ai_result(text: str):
    if not text:
        return False, 0.0
    text = text.strip()

    # 兼容历史提示词输出：相同 / 不同
    if "不同" in text:
        return False, 1.0
    if "相同" in text:
        return True, 1.0

    # 优先按严格JSON解析；失败时尝试提取首个JSON对象。
    result_json = None
    try:
        result_json = json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start >= 0 and end > start:
            try:
                result_json = json.loads(text[start:end + 1])
            except Exception:
                result_json = None

    if not isinstance(result_json, dict):
        return False, 0.0

    same = bool(result_json.get('same', False))
    confidence = result_json.get('confidence', 0)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))
    return same, confidence


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
    if not settings.vul_similarity_ai_enabled:
        return False
    if not settings.openapi_key:
        return False

    descript1 = exists_vul.get('descript', '')
    descript2 = new_vul.get('descript', '')
    _times = _get_vul_time(exists_vul, new_vul)
    exists_vul_publish_time = _times[0]
    new_vul_publish_time = _times[2]

    if not descript1 or not descript2 or not exists_vul_publish_time or not new_vul_publish_time:
        return False

    publish_time_offset = _day_offset(exists_vul_publish_time, new_vul_publish_time)
    if publish_time_offset < 0:
        return False
    if publish_time_offset > settings.vul_similarity_ai_publish_day_diff:
        return False

    try:
        chat_define = settings.vul_similarity_ai_prompt or DEFAULT_AI_PROMPT
        model = settings.openapi_model if settings.openapi_model else DEFAULT_OPENAI_MODEL
        vul_a = _build_ai_payload(exists_vul)
        vul_b = _build_ai_payload(new_vul)
        messages = [
            {"role": "system", "content": chat_define},
            {
                "role": "user",
                "content": json.dumps(
                    {"vul_a": vul_a, "vul_b": vul_b},
                    ensure_ascii=False,
                )
            }
        ]

        # 兼容 openai 新旧 SDK：
        # - 新版使用 OpenAI().chat.completions.create
        # - 旧版使用 openai.ChatCompletion.create
        if hasattr(openai, "OpenAI"):
            kwargs = {"api_key": settings.openapi_key}
            if settings.openapi_base_url:
                kwargs["base_url"] = settings.openapi_base_url
            client = openai.OpenAI(**kwargs)
            completion = client.chat.completions.create(
                model=model,
                temperature=0.4,
                top_p=0.9,
                messages=messages
            )
            result = completion.choices[0].message.content or ''
        else:
            openai.api_key = settings.openapi_key
            if settings.openapi_base_url:
                openai.api_base = settings.openapi_base_url
            completion = openai.ChatCompletion.create(
                model=model,
                temperature=0.4,
                top_p=0.9,
                messages=messages
            )
            result = completion.choices[0].message.content or ''
    except Exception:
        import traceback
        traceback.print_exc()
        result = ''
    same, confidence = _parse_ai_result(result)
    if same and confidence >= settings.vul_similarity_ai_min_confidence:
        return True
    return False


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
    if not words1 or not words2:
        return False
    if words1[0] != words2[0]:
        return False

    # 计算相似度
    sents = macropodus.sim(exists_vul_title, new_vul_title, type_sim="total", type_encode="avg")

    # 如果发布/更新日期相差1天内，则相似度要求降低；否则要求较高
    publish_time_offset = _day_offset(exists_vul_publish_time, new_vul_publish_time)
    update_time_offset = _day_offset(exists_vul_update_time, new_vul_update_time)
    time_window_days = settings.vul_similarity_time_window_days
    time_offset_check = (
        (publish_time_offset >= 0 and publish_time_offset <= time_window_days) or
        (update_time_offset >= 0 and update_time_offset <= time_window_days)
    )

    if (
        sents > settings.vul_similarity_title_threshold_near and time_offset_check
    ) or sents > settings.vul_similarity_title_threshold_far:
        return True
    
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
