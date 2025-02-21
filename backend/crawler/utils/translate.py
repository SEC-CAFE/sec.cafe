#!/usr/bin/env python
# encoding: utf-8

"""
自动识别语言并翻译为中文
"""
import requests
import random
from hashlib import md5

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from src.conf.config import get_app_settings


class Translater(object):
    def __init__(self, engine="auto"):
        # engine: auto(自动轮询)/tencentcloud/baidu/xiaoniu
        self.engines = [""]
        self.engine = engine
        self.source_language = "auto"
        self.target_language = "zh"
        self.settings = get_app_settings()

    def translate(self, source_text):
        engines = {
            "tencentcloud": self.translate_by_tencent,
            "baidu": self.translate_by_baidu,
            "xiaoniu": self.translate_by_xiaoniu
        }
        if self.engine in engines.keys():
            return engines[self.engine](source_text)
        elif self.engine == "auto":
            result = ""
            for _engine, func in engines.items():
                result = func(source_text)
                if result:
                    break
            return result
        else:
            return ""

    def translate_by_tencent(self, source_text):
        secret_id = self.settings.translate_tencent_id
        secret_key = self.settings.translate_tencent_key

        try:
            cred = credential.Credential(secret_id, secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            params = {
                "SourceText": source_text,
                "Source": self.source_language,
                "Target": self.target_language,
                "ProjectId": 0
            }
            common_client = CommonClient("tmt", "2018-03-21", cred, "ap-shanghai", profile=clientProfile)
            result = common_client.call_json("TextTranslate", params)
        except TencentCloudSDKException as err:
            print(err)
            return ""
        else:
            target_text = result.get("Response", {}).get("TargetText", "")
            return target_text

    def translate_by_baidu(self, source_text):
        def make_md5(s, encoding="utf-8"):
            return md5(s.encode(encoding)).hexdigest()
        appid = self.settings.translate_baidu_id
        appkey = self.settings.translate_baidu_key
        endpoint = "http://api.fanyi.baidu.com"
        path = "/api/trans/vip/translate"
        url = endpoint + path

        salt = random.randint(32768, 65536)
        sign = make_md5(appid + source_text + str(salt) + appkey)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "appid": appid,
            "q": source_text,
            "from": self.source_language,
            "to": self.target_language,
            "salt": salt,
            "sign": sign
        }
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        result = result.get("trans_result", [])
        return result[0].get("dst", "") if result else ""

    def translate_by_xiaoniu(self, source_text):
        apikey = self.settings.translate_xiaoniu_key
        url = "http://api.niutrans.com/NiuTransServer/translation"
        payload = {
            "from": self.source_language,
            "to": self.target_language,
            "apikey": apikey,
            "src_text": source_text
        }
        r = requests.post(url, params=payload)
        result = r.json()
        result = result.get("tgt_text", "")
        return result


if __name__ == "__main__":
    T = Translater("auto")
    ret = T.translate("Accellion FTA contains an OS command injection vulnerability exploited via a local web service call.")
    print(ret)
