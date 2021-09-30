from lxml import etree

from configs.settings import redis_client
from games.lottery import random_sign
from utils.chat_api import get_xiaoice_response
from utils.name_recognition import get_place_names
from utils.send_message import send_message
from utils.weather_api import get_date, get_weather


def message_processing(spy, from_wx, from_group_member, content):
    # if from_wx.startwith("gh") == "gh_ab0072172f2d":
    text = ""
    if from_wx.startswith("gh"):
        return
    elif "二猫抽签" in content:
        text = random_sign()
    elif "天气" in content:
        content = content.replace("@二猫", "").strip()
        print(content)
        place = get_place_names(content)
        if place:
            # date = get_date(content)
            text = get_weather(place, content)
        else:
            return
    else:
        if from_wx.endswith("chatroom"):
            if "二猫" not in content:
                return
        text = get_xiaoice_response(spy, content)
        if not text:
            text = "喵喵喵？听不懂啦"
    text.replace("本仙女", "本猫").replace("小冰", "二猫").replace("你女朋友", "你最可爱的小猫咪")
    send_message(spy, from_wx, text)


def xiaoice_message(content):
    xml = etree.XML(content)
    init_url = xml.xpath("string(//url)")
    print(init_url)
    redis_client.set("xiaoice_init_url", init_url)
    # redis_client.set("init_url_status", 1)
