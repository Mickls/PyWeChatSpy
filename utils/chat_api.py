# 访问机器人openapi
# -*- coding: utf-8 -*-
"""
    ChatApis.py
    ~~~~~~~~~

    图灵机器人(公司)闲聊系统API对接
    免费版只限每天调用100次，需联外网

    :date: 2020-02-10 15:56:00
    :author: by jiangdg
"""
import re
import time
from lxml import etree

import requests
import json
import uuid
import random

from configs.settings import REDIS_IP, REDIS_PASSWORD, redis_client, XIAOICE_PHONE, XIAOICE_PASSWORD, XIAOICE_LOGIN_URL, \
    XIAOICE_SEND_MESSAGE_URL, XIAOICE_CROSS_SITE_COLLECTOR_URL, XIAOICE_GET_BATCH_URL
from example_rpc_client import spy

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
    "origin": "https://ux-plus.xiaoice.com",
}
# init_url = "https://ux-plus.xiaoice.com/virtualgirlfriend?feid=81dbe420879b4a6781f52e883778d226&ftid=02803cfc4702ce53789cdfca9113fd4e"
session = requests.session()


# session.get(init_url, headers=headers)


def get_response(msg):
    """
        访问图灵机器人openApi

        :param msg 用户输入的文本消息
        :return string or None
    """
    apiurl = "http://openapi.tuling123.com/openapi/api/v2"
    # 构造请求参数实体
    params = {"reqType": 0,
              "perception": {
                  "inputText": {
                      "text": msg
                  }
              },
              "userInfo": {
                  "apiKey": "ca7bf19ac0e644c38cfbe9d6fdc08de1",
                  "userId": "439608"
              }}
    # 将表单转换为json格式
    content = json.dumps(params)

    # 发起post请求
    r = requests.post(url=apiurl, data=content, verify=False).json()
    print("r = " + str(r))

    # 解析json响应结果
    # {'emotion':{
    #               'robotEmotion': {'a': 0, 'd': 0, 'emotionId': 0, 'p': 0},
    #               'userEmotion': {'a': 0, 'd': 0, 'emotionId': 10300, 'p': 0}
    #            },
    #  'intent': {
    #       'actionName': '',
    #       'code': 10004,
    #       'intentName': ''
    #       },
    #  'results': [{'groupType': 1, 'resultType': 'text', 'values': {'text': '欢迎来到本机器人的地盘。'}}]}
    code = r['intent']['code']
    if code == 10004 or code == 10008:
        message = r['results'][0]['values']['text']
        return message
    return None


def get_xiaoice_init_url():
    init_url = ""
    redis_client.set("init_url_status", 1)
    spy.send_text("gh_ab0072172f2d", "虚拟女友")
    i = 0
    while i < 3:
        time.sleep(2)
        status = redis_client.get("init_url_status")
        if status == "1":
            init_url = redis_client.get("xiaoice_init_url")
            break
        i += 1
    return init_url


def xiaoice_init(init_url):
    global session

    init_res = session.get(init_url, headers=headers)
    init_text = init_res.text
    init_match = re.search("loginInformation=\"https://.*\",t.cros", init_text)
    if not init_match:
        print("init xiaoice failed")
        return False

    auth_url = init_text[init_match.start() + 18: init_match.end() - 7]
    auth_res = session.get(auth_url, headers=headers)
    guest_id = session.cookies.get("SessionGuestId")

    auth_text = auth_res.text
    auth_html = etree.HTML(auth_text)
    auth_token = auth_html.xpath("string(//input[@name='__RequestVerificationToken']/@value)")

    data = {
        "__RequestVerificationToken": auth_token,
        "guestId": guest_id,
        "phone": XIAOICE_PHONE,
        "password": XIAOICE_PASSWORD
    }
    print(data)
    login_res = session.post(XIAOICE_LOGIN_URL, headers=headers, data=data)
    if login_res.status_code == 200:
        init_auth_url = login_res.json()['redirect'].replace("\"", "")
        session.get(init_auth_url, headers=headers)

        headers['referer'] = init_auth_url
        batch_data = ["Management_Entry_Clicked__virtualgirlfriend"]
        batch_res = session.post(XIAOICE_GET_BATCH_URL, json=batch_data, headers=headers)
        if batch_res.status_code != 200:
            print(session.cookies)
            print(batch_res.text)
            print(f"xiaoice batch failed and status_code {batch_res.status_code}")
            return False

        trace_id = uuid.uuid4().hex + str(random.choice(range(10)))
        data = {
            "TraceId": trace_id,
            "PartnerName": "",
            "SubPartnerId": "VirtualGF",
            "Content": {
                "Text": "VirtualGF_MemberJoin",
                "Metadata": {
                    "DisableBehaviorBlock": "True",
                    "H5Enter": "True"
                }
            }
        }
        send_res = session.post(XIAOICE_SEND_MESSAGE_URL, json=data, headers=headers)
        if send_res.status_code != 200:
            print(f"xiaoice login send failed and status_code is {send_res.status_code}")
            return False
        print("xiaoice login success")
        return True
    print(f"xiaoice login failed and status_code is {login_res.status_code}")
    return False


def xiaoice_login():
    init_url = get_xiaoice_init_url()
    if not init_url:
        print("get init url failed")
        return False
    return xiaoice_init(init_url)


def get_xiaoice_response(msg):
    """
    微软小冰api调用
    """

    trace_id = uuid.uuid4().hex + str(random.choice(range(10)))
    data = {
        "TraceId": trace_id,
        "PartnerName": "",
        "SubPartnerId": "VirtualGF",
        "Content": {
            "Text": msg,
            "Metadata": {}
        }
    }

    message = None
    i = 1
    while i < 4:
        try:
            res = session.post(XIAOICE_SEND_MESSAGE_URL, json=data, headers=headers, timeout=(3, 3))
            if res.status_code == 200:
                rsp = res.json()
                message = rsp[0].get("Content", dict()).get("Text")
                if not message:
                    message = "二猫都不知道回你什么好了(＃｀д´)ﾉ"
                break
            elif res.status_code == 401:
                xiaoice_login()
                i += 1
            else:
                break
        except Exception as ex:
            print(ex)
            break
    return message


if __name__ == '__main__':
    if xiaoice_login():
        while True:
            msg = input("msg>>>\n")
            if msg == "q":
                break
            print(get_xiaoice_response(msg))
    else:
        print("error")
# "SessionGuestId"
# "loginInformation=\"https://.*\",t.cros"[+18 - 7]
# "<url><!\[CDATA\[https://.*\]\]></url>"[+14 - 9]
